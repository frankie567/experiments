use anyhow::{Context, Result};
use printpdf::*;
use pulldown_cmark::{Event, Tag, TagEnd};
use std::collections::HashMap;
use std::fs::File;
use std::io::BufWriter;

// Typography settings inspired by LaTeX
const PAGE_WIDTH: f64 = 210.0; // A4 width in mm
const PAGE_HEIGHT: f64 = 297.0; // A4 height in mm
const MARGIN_TOP: f64 = 25.0;
const MARGIN_BOTTOM: f64 = 25.0;
const MARGIN_LEFT: f64 = 25.0;
const MARGIN_RIGHT: f64 = 25.0;

// Text dimensions and positions in mm
const TEXT_WIDTH: f64 = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT;
const TEXT_HEIGHT: f64 = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM;

// Font sizes (in points, converted to mm for printpdf)
const FONT_SIZE_H1: f64 = 18.0;
const FONT_SIZE_H2: f64 = 16.0;
const FONT_SIZE_H3: f64 = 14.0;
const FONT_SIZE_H4: f64 = 12.0;
const FONT_SIZE_H5: f64 = 11.0;
const FONT_SIZE_H6: f64 = 10.0;
const FONT_SIZE_BODY: f64 = 11.0;
const FONT_SIZE_CODE: f64 = 9.0;

// Line height multipliers (LaTeX-like spacing)
const LINE_HEIGHT_H1: f64 = 1.2;
const LINE_HEIGHT_H2: f64 = 1.2;
const LINE_HEIGHT_H3: f64 = 1.15;
const LINE_HEIGHT_BODY: f64 = 1.4;
const LINE_HEIGHT_CODE: f64 = 1.2;

// Spacing (in mm)
const PARAGRAPH_SPACING: f64 = 6.0;
const HEADING_SPACING_BEFORE: f64 = 12.0;
const HEADING_SPACING_AFTER: f64 = 6.0;
const CODE_BLOCK_SPACING: f64 = 8.0;

pub struct PdfRenderer {
    doc: PdfDocumentReference,
    current_page: PdfPageIndex,
    current_layer: PdfLayerIndex,
    current_y: f64,
    fonts: HashMap<String, IndirectFontRef>,
    current_font_size: f64,
    current_line_height: f64,
    page_number: u32,
}

#[derive(Debug, Clone)]
enum TextStyle {
    H1,
    H2,
    H3,
    H4,
    H5,
    H6,
    Body,
    Code,
    Strong,
    Emphasis,
}

impl PdfRenderer {
    pub fn new() -> Result<Self> {
        let (doc, page1, layer1) = PdfDocument::new("Markdown Document", Mm(PAGE_WIDTH as f32), Mm(PAGE_HEIGHT as f32), "Layer 1");
        
        // Load fonts
        let mut fonts = HashMap::new();
        
        // Add built-in fonts
        fonts.insert("regular".to_string(), doc.add_builtin_font(BuiltinFont::TimesRoman)?);
        fonts.insert("bold".to_string(), doc.add_builtin_font(BuiltinFont::TimesBold)?);
        fonts.insert("italic".to_string(), doc.add_builtin_font(BuiltinFont::TimesItalic)?);
        fonts.insert("bold_italic".to_string(), doc.add_builtin_font(BuiltinFont::TimesBoldItalic)?);
        fonts.insert("mono".to_string(), doc.add_builtin_font(BuiltinFont::Courier)?);
        
        Ok(Self {
            doc,
            current_page: page1,
            current_layer: layer1,
            current_y: PAGE_HEIGHT - MARGIN_TOP,
            fonts,
            current_font_size: FONT_SIZE_BODY,
            current_line_height: LINE_HEIGHT_BODY,
            page_number: 1,
        })
    }

    pub fn render_events(&mut self, events: &[Event]) -> Result<()> {
        let mut text_stack = Vec::new();
        let mut in_code_block = false;
        let mut _in_heading = None;
        let mut list_level: u32 = 0;

        for event in events {
            match event {
                Event::Start(tag) => {
                    match tag {
                        Tag::Heading { level, .. } => {
                            self.ensure_space(HEADING_SPACING_BEFORE)?;
                            _in_heading = Some(*level as u32);
                            let style = match level {
                                pulldown_cmark::HeadingLevel::H1 => TextStyle::H1,
                                pulldown_cmark::HeadingLevel::H2 => TextStyle::H2,
                                pulldown_cmark::HeadingLevel::H3 => TextStyle::H3,
                                pulldown_cmark::HeadingLevel::H4 => TextStyle::H4,
                                pulldown_cmark::HeadingLevel::H5 => TextStyle::H5,
                                pulldown_cmark::HeadingLevel::H6 => TextStyle::H6,
                            };
                            self.set_text_style(&style);
                        },
                        Tag::Paragraph => {
                            self.ensure_space(PARAGRAPH_SPACING / 2.0)?;
                            self.set_text_style(&TextStyle::Body);
                        },
                        Tag::CodeBlock(_) => {
                            self.ensure_space(CODE_BLOCK_SPACING)?;
                            in_code_block = true;
                            self.set_text_style(&TextStyle::Code);
                        },
                        Tag::List(_) => {
                            list_level += 1;
                            self.ensure_space(PARAGRAPH_SPACING / 2.0)?;
                        },
                        Tag::Item => {
                            // Add bullet point or number
                            let indent = (list_level - 1) as f64 * 10.0;
                            let bullet = if list_level == 1 { "•" } else { "◦" };
                            self.add_text_at_position(&bullet, MARGIN_LEFT + indent, self.current_y)?;
                        },
                        Tag::Strong => {
                            text_stack.push(TextStyle::Strong);
                        },
                        Tag::Emphasis => {
                            text_stack.push(TextStyle::Emphasis);
                        },
                        _ => {}
                    }
                },
                Event::End(tag_end) => {
                    match tag_end {
                        TagEnd::Heading(_) => {
                            _in_heading = None;
                            self.ensure_space(HEADING_SPACING_AFTER)?;
                            self.set_text_style(&TextStyle::Body);
                        },
                        TagEnd::Paragraph => {
                            self.ensure_space(PARAGRAPH_SPACING / 2.0)?;
                        },
                        TagEnd::CodeBlock => {
                            in_code_block = false;
                            self.ensure_space(CODE_BLOCK_SPACING)?;
                            self.set_text_style(&TextStyle::Body);
                        },
                        TagEnd::List(_) => {
                            list_level = list_level.saturating_sub(1);
                            self.ensure_space(PARAGRAPH_SPACING / 2.0)?;
                        },
                        TagEnd::Strong | TagEnd::Emphasis => {
                            text_stack.pop();
                        },
                        _ => {}
                    }
                },
                Event::Text(text) => {
                    if in_code_block {
                        self.add_code_block(&text)?;
                    } else {
                        let indent = if list_level > 0 {
                            (list_level as f64) * 10.0
                        } else {
                            0.0
                        };
                        self.add_text_with_indent(&text, indent)?;
                    }
                },
                Event::Code(code) => {
                    self.add_inline_code(&code)?;
                },
                Event::SoftBreak => {
                    self.add_text(" ")?;
                },
                Event::HardBreak => {
                    self.new_line()?;
                },
                _ => {}
            }
        }

        Ok(())
    }

    fn set_text_style(&mut self, style: &TextStyle) {
        match style {
            TextStyle::H1 => {
                self.current_font_size = FONT_SIZE_H1;
                self.current_line_height = LINE_HEIGHT_H1;
            },
            TextStyle::H2 => {
                self.current_font_size = FONT_SIZE_H2;
                self.current_line_height = LINE_HEIGHT_H2;
            },
            TextStyle::H3 => {
                self.current_font_size = FONT_SIZE_H3;
                self.current_line_height = LINE_HEIGHT_H3;
            },
            TextStyle::H4 => {
                self.current_font_size = FONT_SIZE_H4;
                self.current_line_height = LINE_HEIGHT_BODY;
            },
            TextStyle::H5 => {
                self.current_font_size = FONT_SIZE_H5;
                self.current_line_height = LINE_HEIGHT_BODY;
            },
            TextStyle::H6 => {
                self.current_font_size = FONT_SIZE_H6;
                self.current_line_height = LINE_HEIGHT_BODY;
            },
            TextStyle::Body => {
                self.current_font_size = FONT_SIZE_BODY;
                self.current_line_height = LINE_HEIGHT_BODY;
            },
            TextStyle::Code => {
                self.current_font_size = FONT_SIZE_CODE;
                self.current_line_height = LINE_HEIGHT_CODE;
            },
            _ => {} // Other styles handled by font selection
        }
    }

    fn get_font_for_style(&self, style: &TextStyle) -> &IndirectFontRef {
        match style {
            TextStyle::Code => &self.fonts["mono"],
            TextStyle::Strong => &self.fonts["bold"],
            TextStyle::Emphasis => &self.fonts["italic"],
            TextStyle::H1 | TextStyle::H2 | TextStyle::H3 => &self.fonts["bold"],
            _ => &self.fonts["regular"],
        }
    }

    fn ensure_space(&mut self, space: f64) -> Result<()> {
        if self.current_y - space < MARGIN_BOTTOM {
            self.new_page()?;
        } else {
            self.current_y -= space;
        }
        Ok(())
    }

    fn new_page(&mut self) -> Result<()> {
        self.page_number += 1;
        let (page, layer) = self.doc.add_page(Mm(PAGE_WIDTH as f32), Mm(PAGE_HEIGHT as f32), "Layer 1");
        self.current_page = page;
        self.current_layer = layer;
        self.current_y = PAGE_HEIGHT - MARGIN_TOP;
        
        // Add page number
        let layer_ref = self.doc.get_page(self.current_page).get_layer(self.current_layer);
        layer_ref.use_text(
            &format!("- {} -", self.page_number), 
            8.0, 
            Mm((PAGE_WIDTH / 2.0 - 10.0) as f32), 
            Mm((MARGIN_BOTTOM / 2.0) as f32), 
            &self.fonts["regular"]
        );
        
        Ok(())
    }

    fn new_line(&mut self) -> Result<()> {
        let line_spacing = self.current_font_size * self.current_line_height * 0.352777778; // Convert pt to mm
        self.ensure_space(line_spacing)?;
        Ok(())
    }

    fn add_text(&mut self, text: &str) -> Result<()> {
        self.add_text_with_indent(text, 0.0)
    }

    fn add_text_with_indent(&mut self, text: &str, indent: f64) -> Result<()> {
        let lines = self.wrap_text(text, TEXT_WIDTH - indent);
        
        for line in lines {
            if !line.trim().is_empty() {
                self.add_text_at_position(&line, MARGIN_LEFT + indent, self.current_y)?;
            }
            self.new_line()?;
        }
        
        Ok(())
    }

    fn add_text_at_position(&mut self, text: &str, x: f64, y: f64) -> Result<()> {
        let layer_ref = self.doc.get_page(self.current_page).get_layer(self.current_layer);
        let font = self.get_font_for_style(&TextStyle::Body); // Default to body style
        
        layer_ref.use_text(text, self.current_font_size as f32, Mm(x as f32), Mm(y as f32), font);
        Ok(())
    }

    fn add_code_block(&mut self, code: &str) -> Result<()> {
        let lines: Vec<&str> = code.lines().collect();
        
        for line in lines {
            let layer_ref = self.doc.get_page(self.current_page).get_layer(self.current_layer);
            layer_ref.use_text(
                line, 
                self.current_font_size as f32, 
                Mm((MARGIN_LEFT + 5.0) as f32), // Slight indent for code blocks
                Mm(self.current_y as f32), 
                &self.fonts["mono"]
            );
            self.new_line()?;
        }
        
        Ok(())
    }

    fn add_inline_code(&mut self, code: &str) -> Result<()> {
        let layer_ref = self.doc.get_page(self.current_page).get_layer(self.current_layer);
        layer_ref.use_text(code, (self.current_font_size * 0.9) as f32, Mm(MARGIN_LEFT as f32), Mm(self.current_y as f32), &self.fonts["mono"]);
        Ok(())
    }

    fn wrap_text(&self, text: &str, max_width: f64) -> Vec<String> {
        // Simple word wrapping - in a real implementation, you'd want proper text measurement
        let words: Vec<&str> = text.split_whitespace().collect();
        let mut lines = Vec::new();
        let mut current_line = String::new();
        
        // Rough character width estimation (this is very approximate)
        let approx_char_width = self.current_font_size * 0.5 * 0.352777778; // Convert pt to mm
        let max_chars = (max_width / approx_char_width) as usize;
        
        for word in words {
            if current_line.len() + word.len() + 1 > max_chars && !current_line.is_empty() {
                lines.push(current_line.clone());
                current_line = word.to_string();
            } else {
                if !current_line.is_empty() {
                    current_line.push(' ');
                }
                current_line.push_str(word);
            }
        }
        
        if !current_line.is_empty() {
            lines.push(current_line);
        }
        
        if lines.is_empty() {
            lines.push(String::new());
        }
        
        lines
    }

    pub fn save_to_file(self, path: &str) -> Result<()> {
        let file = File::create(path)?;
        let mut writer = BufWriter::new(file);
        self.doc.save(&mut writer).context("Failed to save PDF")?;
        Ok(())
    }
}