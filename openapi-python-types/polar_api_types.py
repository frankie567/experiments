from __future__ import annotations
from typing import Any, Literal, NotRequired, TypedDict, overload

class Address(TypedDict):
    line1: NotRequired[str | None]
    line2: NotRequired[str | None]
    postal_code: NotRequired[str | None]
    city: NotRequired[str | None]
    state: NotRequired[str | None]
    country: Literal['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW']

class AddressDict(TypedDict):
    line1: NotRequired[str]
    line2: NotRequired[str]
    postal_code: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    country: str

class AddressInput(TypedDict):
    line1: NotRequired[str | None]
    line2: NotRequired[str | None]
    postal_code: NotRequired[str | None]
    city: NotRequired[str | None]
    state: NotRequired[str | None]
    country: Literal['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW']

class AlreadyActiveSubscriptionError(TypedDict):
    error: Literal['AlreadyActiveSubscriptionError']
    detail: str

class AlreadyCanceledSubscription(TypedDict):
    error: Literal['AlreadyCanceledSubscription']
    detail: str

class AttachedCustomField(TypedDict):
    """Schema of a custom field attached to a resource."""
    custom_field_id: str
    custom_field: CustomField
    order: int
    required: bool

class AttachedCustomFieldCreate(TypedDict):
    """Schema to attach a custom field to a resource."""
    custom_field_id: str
    required: bool

class AuthorizeOrganization(TypedDict):
    id: str
    slug: str
    avatar_url: str | None

class AuthorizeResponseOrganization(TypedDict):
    client: OAuth2ClientPublic
    sub_type: Literal['organization']
    sub: AuthorizeOrganization | None
    scopes: list[Scope]
    scope_display_names: NotRequired[dict[str, Any]]
    organizations: list[AuthorizeOrganization]

class AuthorizeResponseUser(TypedDict):
    client: OAuth2ClientPublic
    sub_type: Literal['user']
    sub: AuthorizeUser | None
    scopes: list[Scope]
    scope_display_names: NotRequired[dict[str, Any]]

class AuthorizeUser(TypedDict):
    id: str
    email: str
    avatar_url: str | None

class BalanceCreditOrderEvent(TypedDict):
    """An event created by Polar when an order is paid via customer balance."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['balance.credit_order']
    metadata: BalanceCreditOrderMetadata

class BalanceCreditOrderMetadata(TypedDict):
    order_id: str
    product_id: NotRequired[str]
    subscription_id: NotRequired[str]
    amount: int
    currency: str
    tax_amount: int
    tax_state: NotRequired[str | None]
    tax_country: NotRequired[str | None]
    fee: int

class BalanceDisputeEvent(TypedDict):
    """An event created by Polar when an order is disputed."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['balance.dispute']
    metadata: BalanceDisputeMetadata

class BalanceDisputeMetadata(TypedDict):
    transaction_id: str
    dispute_id: str
    order_id: NotRequired[str]
    order_created_at: NotRequired[str]
    product_id: NotRequired[str]
    subscription_id: NotRequired[str]
    amount: int
    currency: str
    presentment_amount: int
    presentment_currency: str
    tax_amount: int
    tax_state: NotRequired[str | None]
    tax_country: NotRequired[str | None]
    fee: int
    exchange_rate: NotRequired[float]

class BalanceDisputeReversalEvent(TypedDict):
    """An event created by Polar when a dispute is won and funds are reinstated."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['balance.dispute_reversal']
    metadata: BalanceDisputeMetadata

class BalanceOrderEvent(TypedDict):
    """An event created by Polar when an order is paid."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['balance.order']
    metadata: BalanceOrderMetadata

class BalanceOrderMetadata(TypedDict):
    transaction_id: str
    order_id: str
    product_id: NotRequired[str]
    subscription_id: NotRequired[str]
    amount: int
    net_amount: NotRequired[int]
    currency: str
    presentment_amount: int
    presentment_currency: str
    tax_amount: int
    tax_state: NotRequired[str | None]
    tax_country: NotRequired[str | None]
    fee: int
    exchange_rate: NotRequired[float]

class BalanceRefundEvent(TypedDict):
    """An event created by Polar when an order is refunded."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['balance.refund']
    metadata: BalanceRefundMetadata

class BalanceRefundMetadata(TypedDict):
    transaction_id: str
    refund_id: str
    order_id: NotRequired[str]
    order_created_at: NotRequired[str]
    product_id: NotRequired[str]
    subscription_id: NotRequired[str]
    amount: int
    currency: str
    presentment_amount: int
    presentment_currency: str
    refundable_amount: NotRequired[int]
    tax_amount: int
    tax_state: NotRequired[str | None]
    tax_country: NotRequired[str | None]
    fee: int
    exchange_rate: NotRequired[float]

class BalanceRefundReversalEvent(TypedDict):
    """An event created by Polar when a refund is reverted."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['balance.refund_reversal']
    metadata: BalanceRefundMetadata

class BenefitCustom(TypedDict):
    """A benefit of type `custom`.

Use it to grant any kind of benefit that doesn't fit in the other types."""
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['custom']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    properties: BenefitCustomProperties

class BenefitCustomCreate(TypedDict):
    """Schema to create a benefit of type `custom`."""
    metadata: NotRequired[dict[str, Any]]
    type: Literal['custom']
    description: str
    organization_id: NotRequired[str | None]
    properties: BenefitCustomCreateProperties

class BenefitCustomCreateProperties(TypedDict):
    """Properties for creating a benefit of type `custom`."""
    note: NotRequired[str | None | None]

class BenefitCustomProperties(TypedDict):
    """Properties for a benefit of type `custom`."""
    note: str | None | None

class BenefitCustomSubscriber(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['custom']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    organization: BenefitSubscriberOrganization
    properties: BenefitCustomSubscriberProperties

class BenefitCustomSubscriberProperties(TypedDict):
    """Properties available to subscribers for a benefit of type `custom`."""
    note: str | None | None

class BenefitCustomUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    description: NotRequired[str | None]
    type: Literal['custom']
    properties: NotRequired[BenefitCustomProperties | None]

class BenefitCycledEvent(TypedDict):
    """An event created by Polar when a benefit is cycled."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['benefit.cycled']
    metadata: BenefitGrantMetadata

class BenefitDiscord(TypedDict):
    """A benefit of type `discord`.

Use it to automatically invite your backers to a Discord server."""
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['discord']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    properties: BenefitDiscordProperties

class BenefitDiscordCreate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    type: Literal['discord']
    description: str
    organization_id: NotRequired[str | None]
    properties: BenefitDiscordCreateProperties

class BenefitDiscordCreateProperties(TypedDict):
    """Properties to create a benefit of type `discord`."""
    guild_token: str
    role_id: str
    kick_member: bool

class BenefitDiscordProperties(TypedDict):
    """Properties for a benefit of type `discord`."""
    guild_id: str
    role_id: str
    kick_member: bool
    guild_token: str

class BenefitDiscordSubscriber(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['discord']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    organization: BenefitSubscriberOrganization
    properties: BenefitDiscordSubscriberProperties

class BenefitDiscordSubscriberProperties(TypedDict):
    """Properties available to subscribers for a benefit of type `discord`."""
    guild_id: str

class BenefitDiscordUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    description: NotRequired[str | None]
    type: Literal['discord']
    properties: NotRequired[BenefitDiscordCreateProperties | None]

class BenefitDownloadables(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['downloadables']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    properties: BenefitDownloadablesProperties

class BenefitDownloadablesCreate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    type: Literal['downloadables']
    description: str
    organization_id: NotRequired[str | None]
    properties: BenefitDownloadablesCreateProperties

class BenefitDownloadablesCreateProperties(TypedDict):
    archived: NotRequired[dict[str, Any]]
    files: list[str]

class BenefitDownloadablesProperties(TypedDict):
    archived: dict[str, Any]
    files: list[str]

class BenefitDownloadablesSubscriber(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['downloadables']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    organization: BenefitSubscriberOrganization
    properties: BenefitDownloadablesSubscriberProperties

class BenefitDownloadablesSubscriberProperties(TypedDict):
    active_files: list[str]

class BenefitDownloadablesUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    description: NotRequired[str | None]
    type: Literal['downloadables']
    properties: NotRequired[BenefitDownloadablesCreateProperties | None]

class BenefitGitHubRepository(TypedDict):
    """A benefit of type `github_repository`.

Use it to automatically invite your backers to a private GitHub repository."""
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['github_repository']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    properties: BenefitGitHubRepositoryProperties

class BenefitGitHubRepositoryCreate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    type: Literal['github_repository']
    description: str
    organization_id: NotRequired[str | None]
    properties: BenefitGitHubRepositoryCreateProperties

class BenefitGitHubRepositoryCreateProperties(TypedDict):
    """Properties to create a benefit of type `github_repository`."""
    repository_owner: str
    repository_name: str
    permission: Literal['pull', 'triage', 'push', 'maintain', 'admin']

class BenefitGitHubRepositoryProperties(TypedDict):
    """Properties for a benefit of type `github_repository`."""
    repository_owner: str
    repository_name: str
    permission: Literal['pull', 'triage', 'push', 'maintain', 'admin']

class BenefitGitHubRepositorySubscriber(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['github_repository']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    organization: BenefitSubscriberOrganization
    properties: BenefitGitHubRepositorySubscriberProperties

class BenefitGitHubRepositorySubscriberProperties(TypedDict):
    """Properties available to subscribers for a benefit of type `github_repository`."""
    repository_owner: str
    repository_name: str

class BenefitGitHubRepositoryUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    description: NotRequired[str | None]
    type: Literal['github_repository']
    properties: NotRequired[BenefitGitHubRepositoryCreateProperties | None]

class BenefitGrant(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: NotRequired[str | None]
    is_granted: bool
    revoked_at: NotRequired[str | None]
    is_revoked: bool
    subscription_id: str | None
    order_id: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    error: NotRequired[BenefitGrantError | None]
    customer: Customer
    member: NotRequired[Member | None]
    benefit: Benefit
    properties: BenefitGrantDiscordProperties | BenefitGrantGitHubRepositoryProperties | BenefitGrantDownloadablesProperties | BenefitGrantLicenseKeysProperties | BenefitGrantCustomProperties

class BenefitGrantCustomProperties(TypedDict):
    pass

class BenefitGrantCustomWebhook(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: NotRequired[str | None]
    is_granted: bool
    revoked_at: NotRequired[str | None]
    is_revoked: bool
    subscription_id: str | None
    order_id: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    error: NotRequired[BenefitGrantError | None]
    customer: Customer
    member: NotRequired[Member | None]
    benefit: BenefitCustom
    properties: BenefitGrantCustomProperties
    previous_properties: NotRequired[BenefitGrantCustomProperties | None]

class BenefitGrantDiscordProperties(TypedDict):
    account_id: NotRequired[str | None]
    guild_id: NotRequired[str]
    role_id: NotRequired[str]
    granted_account_id: NotRequired[str]

class BenefitGrantDiscordWebhook(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: NotRequired[str | None]
    is_granted: bool
    revoked_at: NotRequired[str | None]
    is_revoked: bool
    subscription_id: str | None
    order_id: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    error: NotRequired[BenefitGrantError | None]
    customer: Customer
    member: NotRequired[Member | None]
    benefit: BenefitDiscord
    properties: BenefitGrantDiscordProperties
    previous_properties: NotRequired[BenefitGrantDiscordProperties | None]

class BenefitGrantDownloadablesProperties(TypedDict):
    files: NotRequired[list[str]]

class BenefitGrantDownloadablesWebhook(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: NotRequired[str | None]
    is_granted: bool
    revoked_at: NotRequired[str | None]
    is_revoked: bool
    subscription_id: str | None
    order_id: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    error: NotRequired[BenefitGrantError | None]
    customer: Customer
    member: NotRequired[Member | None]
    benefit: BenefitDownloadables
    properties: BenefitGrantDownloadablesProperties
    previous_properties: NotRequired[BenefitGrantDownloadablesProperties | None]

class BenefitGrantError(TypedDict):
    message: str
    type: str
    timestamp: str

class BenefitGrantGitHubRepositoryProperties(TypedDict):
    account_id: NotRequired[str | None]
    repository_owner: NotRequired[str]
    repository_name: NotRequired[str]
    permission: NotRequired[Literal['pull', 'triage', 'push', 'maintain', 'admin']]
    granted_account_id: NotRequired[str]

class BenefitGrantGitHubRepositoryWebhook(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: NotRequired[str | None]
    is_granted: bool
    revoked_at: NotRequired[str | None]
    is_revoked: bool
    subscription_id: str | None
    order_id: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    error: NotRequired[BenefitGrantError | None]
    customer: Customer
    member: NotRequired[Member | None]
    benefit: BenefitGitHubRepository
    properties: BenefitGrantGitHubRepositoryProperties
    previous_properties: NotRequired[BenefitGrantGitHubRepositoryProperties | None]

class BenefitGrantLicenseKeysProperties(TypedDict):
    user_provided_key: NotRequired[str]
    license_key_id: NotRequired[str]
    display_key: NotRequired[str]

class BenefitGrantLicenseKeysWebhook(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: NotRequired[str | None]
    is_granted: bool
    revoked_at: NotRequired[str | None]
    is_revoked: bool
    subscription_id: str | None
    order_id: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    error: NotRequired[BenefitGrantError | None]
    customer: Customer
    member: NotRequired[Member | None]
    benefit: BenefitLicenseKeys
    properties: BenefitGrantLicenseKeysProperties
    previous_properties: NotRequired[BenefitGrantLicenseKeysProperties | None]

class BenefitGrantMetadata(TypedDict):
    benefit_id: str
    benefit_grant_id: str
    benefit_type: BenefitType
    member_id: NotRequired[str]

class BenefitGrantMeterCreditProperties(TypedDict):
    last_credited_meter_id: NotRequired[str]
    last_credited_units: NotRequired[int]
    last_credited_at: NotRequired[str]

class BenefitGrantMeterCreditWebhook(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: NotRequired[str | None]
    is_granted: bool
    revoked_at: NotRequired[str | None]
    is_revoked: bool
    subscription_id: str | None
    order_id: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    error: NotRequired[BenefitGrantError | None]
    customer: Customer
    member: NotRequired[Member | None]
    benefit: BenefitMeterCredit
    properties: BenefitGrantMeterCreditProperties
    previous_properties: NotRequired[BenefitGrantMeterCreditProperties | None]

class BenefitGrantedEvent(TypedDict):
    """An event created by Polar when a benefit is granted to a customer."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['benefit.granted']
    metadata: BenefitGrantMetadata

class BenefitLicenseKeyActivationCreateProperties(TypedDict):
    limit: int
    enable_customer_admin: bool

class BenefitLicenseKeyActivationProperties(TypedDict):
    limit: int
    enable_customer_admin: bool

class BenefitLicenseKeyExpirationProperties(TypedDict):
    ttl: int
    timeframe: Literal['year', 'month', 'day']

class BenefitLicenseKeys(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['license_keys']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    properties: BenefitLicenseKeysProperties

class BenefitLicenseKeysCreate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    type: Literal['license_keys']
    description: str
    organization_id: NotRequired[str | None]
    properties: BenefitLicenseKeysCreateProperties

class BenefitLicenseKeysCreateProperties(TypedDict):
    prefix: NotRequired[str | None]
    expires: NotRequired[BenefitLicenseKeyExpirationProperties | None]
    activations: NotRequired[BenefitLicenseKeyActivationCreateProperties | None]
    limit_usage: NotRequired[int | None]

class BenefitLicenseKeysProperties(TypedDict):
    prefix: str | None
    expires: BenefitLicenseKeyExpirationProperties | None
    activations: BenefitLicenseKeyActivationProperties | None
    limit_usage: int | None

class BenefitLicenseKeysSubscriber(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['license_keys']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    organization: BenefitSubscriberOrganization
    properties: BenefitLicenseKeysSubscriberProperties

class BenefitLicenseKeysSubscriberProperties(TypedDict):
    prefix: str | None
    expires: BenefitLicenseKeyExpirationProperties | None
    activations: BenefitLicenseKeyActivationProperties | None
    limit_usage: int | None

class BenefitLicenseKeysUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    description: NotRequired[str | None]
    type: Literal['license_keys']
    properties: NotRequired[BenefitLicenseKeysCreateProperties | None]

class BenefitMeterCredit(TypedDict):
    """A benefit of type `meter_unit`.

Use it to grant a number of units on a specific meter."""
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['meter_credit']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    properties: BenefitMeterCreditProperties

class BenefitMeterCreditCreate(TypedDict):
    """Schema to create a benefit of type `meter_unit`."""
    metadata: NotRequired[dict[str, Any]]
    type: Literal['meter_credit']
    description: str
    organization_id: NotRequired[str | None]
    properties: BenefitMeterCreditCreateProperties

class BenefitMeterCreditCreateProperties(TypedDict):
    """Properties for creating a benefit of type `meter_unit`."""
    units: int
    rollover: bool
    meter_id: str

class BenefitMeterCreditProperties(TypedDict):
    """Properties for a benefit of type `meter_unit`."""
    units: int
    rollover: bool
    meter_id: str

class BenefitMeterCreditSubscriber(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: Literal['meter_credit']
    description: str
    selectable: bool
    deletable: bool
    organization_id: str
    metadata: MetadataOutputType
    organization: BenefitSubscriberOrganization
    properties: BenefitMeterCreditSubscriberProperties

class BenefitMeterCreditSubscriberProperties(TypedDict):
    """Properties available to subscribers for a benefit of type `meter_unit`."""
    units: int
    rollover: bool
    meter_id: str

class BenefitMeterCreditUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    description: NotRequired[str | None]
    type: Literal['meter_credit']
    properties: NotRequired[BenefitMeterCreditCreateProperties | None]

class BenefitPublic(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    type: BenefitType
    description: str
    selectable: bool
    deletable: bool
    organization_id: str

class BenefitRevokedEvent(TypedDict):
    """An event created by Polar when a benefit is revoked from a customer."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['benefit.revoked']
    metadata: BenefitGrantMetadata

class BenefitSubscriberOrganization(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str
    slug: str
    avatar_url: str | None
    proration_behavior: SubscriptionProrationBehavior
    allow_customer_updates: bool

class BenefitUpdatedEvent(TypedDict):
    """An event created by Polar when a benefit is updated."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['benefit.updated']
    metadata: BenefitGrantMetadata

class CardPayment(TypedDict):
    """Schema of a payment with a card payment method."""
    created_at: str
    modified_at: str | None
    id: str
    processor: PaymentProcessor
    status: PaymentStatus
    amount: int
    currency: str
    method: Literal['card']
    decline_reason: str | None
    decline_message: str | None
    organization_id: str
    checkout_id: str | None
    order_id: str | None
    processor_metadata: NotRequired[dict[str, Any]]
    method_metadata: CardPaymentMetadata

class CardPaymentMetadata(TypedDict):
    """Additional metadata for a card payment method."""
    brand: str
    last4: str

class Checkout(TypedDict):
    """Checkout session data retrieved using an access token."""
    id: str
    created_at: str
    modified_at: str | None
    custom_field_data: NotRequired[dict[str, Any]]
    payment_processor: PaymentProcessor
    status: CheckoutStatus
    client_secret: str
    url: str
    expires_at: str
    success_url: str
    return_url: str | None
    embed_origin: str | None
    amount: int
    seats: NotRequired[int | None]
    price_per_seat: NotRequired[int | None]
    discount_amount: int
    net_amount: int
    tax_amount: int | None
    total_amount: int
    currency: str
    allow_trial: bool | None
    active_trial_interval: TrialInterval | None
    active_trial_interval_count: int | None
    trial_end: str | None
    organization_id: str
    product_id: str | None
    product_price_id: str | None
    discount_id: str | None
    allow_discount_codes: bool
    require_billing_address: bool
    is_discount_applicable: bool
    is_free_product_price: bool
    is_payment_required: bool
    is_payment_setup_required: bool
    is_payment_form_required: bool
    customer_id: str | None
    is_business_customer: bool
    customer_name: str | None
    customer_email: str | None
    customer_ip_address: str | None
    customer_billing_name: str | None
    customer_billing_address: Address | None
    customer_tax_id: str | None
    locale: NotRequired[str | None]
    payment_processor_metadata: dict[str, Any]
    billing_address_fields: CheckoutBillingAddressFields
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    metadata: MetadataOutputType
    external_customer_id: str | None
    customer_external_id: str | None
    products: list[CheckoutProduct]
    product: CheckoutProduct | None
    product_price: LegacyRecurringProductPrice | ProductPrice | None
    prices: dict[str, Any] | None
    discount: CheckoutDiscountFixedOnceForeverDuration | CheckoutDiscountFixedRepeatDuration | CheckoutDiscountPercentageOnceForeverDuration | CheckoutDiscountPercentageRepeatDuration | None
    subscription_id: str | None
    attached_custom_fields: list[AttachedCustomField] | None
    customer_metadata: dict[str, Any]

class CheckoutBillingAddressFields(TypedDict):
    country: BillingAddressFieldMode
    state: BillingAddressFieldMode
    city: BillingAddressFieldMode
    postal_code: BillingAddressFieldMode
    line1: BillingAddressFieldMode
    line2: BillingAddressFieldMode

class CheckoutConfirmStripe(TypedDict):
    """Confirm a checkout session using a Stripe confirmation token."""
    custom_field_data: NotRequired[dict[str, Any]]
    product_id: NotRequired[str | None]
    product_price_id: NotRequired[str | None]
    amount: NotRequired[int | None]
    seats: NotRequired[int | None]
    is_business_customer: NotRequired[bool | None]
    customer_name: NotRequired[str | None]
    customer_email: NotRequired[str | None]
    customer_billing_name: NotRequired[str | None]
    customer_billing_address: NotRequired[AddressInput | None]
    customer_tax_id: NotRequired[str | None]
    locale: NotRequired[str | None]
    discount_code: NotRequired[str | None]
    allow_trial: NotRequired[Literal[False] | None]
    confirmation_token_id: NotRequired[str | None]

class CheckoutCreatedEvent(TypedDict):
    """An event created by Polar when a checkout is created."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['checkout.created']
    metadata: CheckoutCreatedMetadata

class CheckoutCreatedMetadata(TypedDict):
    checkout_id: str
    checkout_status: str
    product_id: NotRequired[str]

class CheckoutCustomerBillingAddressFields(TypedDict):
    """Deprecated: Use CheckoutBillingAddressFields instead."""
    country: bool
    state: bool
    city: bool
    postal_code: bool
    line1: bool
    line2: bool

class CheckoutDiscountFixedOnceForeverDuration(TypedDict):
    """Schema for a fixed amount discount that is applied once or forever."""
    duration: DiscountDuration
    type: DiscountType
    amount: int
    currency: str
    id: str
    name: str
    code: str | None

class CheckoutDiscountFixedRepeatDuration(TypedDict):
    """Schema for a fixed amount discount that is applied on every invoice
for a certain number of months."""
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    amount: int
    currency: str
    id: str
    name: str
    code: str | None

class CheckoutDiscountPercentageOnceForeverDuration(TypedDict):
    """Schema for a percentage discount that is applied once or forever."""
    duration: DiscountDuration
    type: DiscountType
    basis_points: int
    id: str
    name: str
    code: str | None

class CheckoutDiscountPercentageRepeatDuration(TypedDict):
    """Schema for a percentage discount that is applied on every invoice
for a certain number of months."""
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    basis_points: int
    id: str
    name: str
    code: str | None

class CheckoutLink(TypedDict):
    """Checkout link data."""
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    metadata: MetadataOutputType
    payment_processor: PaymentProcessor
    client_secret: str
    success_url: str | None
    label: str | None
    allow_discount_codes: bool
    require_billing_address: bool
    discount_id: str | None
    organization_id: str
    products: list[CheckoutLinkProduct]
    discount: DiscountFixedOnceForeverDurationBase | DiscountFixedRepeatDurationBase | DiscountPercentageOnceForeverDurationBase | DiscountPercentageRepeatDurationBase | None
    url: str

class CheckoutLinkCreateProduct(TypedDict):
    """Schema to create a new checkout link from a a single product.

**Deprecated**: Use `CheckoutLinkCreateProducts` instead."""
    metadata: NotRequired[dict[str, Any]]
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    payment_processor: Literal['stripe']
    label: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool]
    require_billing_address: NotRequired[bool]
    discount_id: NotRequired[str | None]
    success_url: NotRequired[str | None]
    product_id: str

class CheckoutLinkCreateProductPrice(TypedDict):
    """Schema to create a new checkout link from a a single product price.

**Deprecated**: Use `CheckoutLinkCreateProducts` instead."""
    metadata: NotRequired[dict[str, Any]]
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    payment_processor: Literal['stripe']
    label: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool]
    require_billing_address: NotRequired[bool]
    discount_id: NotRequired[str | None]
    success_url: NotRequired[str | None]
    product_price_id: str

class CheckoutLinkCreateProducts(TypedDict):
    """Schema to create a new checkout link."""
    metadata: NotRequired[dict[str, Any]]
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    payment_processor: Literal['stripe']
    label: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool]
    require_billing_address: NotRequired[bool]
    discount_id: NotRequired[str | None]
    success_url: NotRequired[str | None]
    products: list[str]

class CheckoutLinkProduct(TypedDict):
    """Product data for a checkout link."""
    metadata: MetadataOutputType
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    benefits: list[BenefitPublic]
    medias: list[ProductMediaFileRead]

class CheckoutLinkUpdate(TypedDict):
    """Schema to update an existing checkout link."""
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    metadata: NotRequired[dict[str, Any]]
    products: NotRequired[list[str] | None]
    label: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool | None]
    require_billing_address: NotRequired[bool | None]
    discount_id: NotRequired[str | None]
    success_url: NotRequired[str | None]

class CheckoutOrganization(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str
    slug: str
    avatar_url: str | None
    proration_behavior: SubscriptionProrationBehavior
    allow_customer_updates: bool

class CheckoutPriceCreate(TypedDict):
    """Create a new checkout session from a product price.

**Deprecated**: Use `CheckoutProductsCreate` instead.

Metadata set on the checkout will be copied
to the resulting order and/or subscription."""
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    metadata: NotRequired[dict[str, Any]]
    custom_field_data: NotRequired[dict[str, Any]]
    discount_id: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool]
    require_billing_address: NotRequired[bool]
    amount: NotRequired[int | None]
    seats: NotRequired[int | None]
    allow_trial: NotRequired[bool]
    customer_id: NotRequired[str | None]
    is_business_customer: NotRequired[bool]
    external_customer_id: NotRequired[str | None]
    customer_name: NotRequired[str | None]
    customer_email: NotRequired[str | None]
    customer_ip_address: NotRequired[str | None]
    customer_billing_name: NotRequired[str | None]
    customer_billing_address: NotRequired[AddressInput | None]
    customer_tax_id: NotRequired[str | None]
    customer_metadata: NotRequired[dict[str, Any]]
    subscription_id: NotRequired[str | None]
    success_url: NotRequired[str | None]
    return_url: NotRequired[str | None]
    embed_origin: NotRequired[str | None]
    locale: NotRequired[str | None]
    product_price_id: str

class CheckoutProduct(TypedDict):
    """Product data for a checkout session."""
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    benefits: list[BenefitPublic]
    medias: list[ProductMediaFileRead]

class CheckoutProductCreate(TypedDict):
    """Create a new checkout session from a product.

**Deprecated**: Use `CheckoutProductsCreate` instead.

Metadata set on the checkout will be copied
to the resulting order and/or subscription."""
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    metadata: NotRequired[dict[str, Any]]
    custom_field_data: NotRequired[dict[str, Any]]
    discount_id: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool]
    require_billing_address: NotRequired[bool]
    amount: NotRequired[int | None]
    seats: NotRequired[int | None]
    allow_trial: NotRequired[bool]
    customer_id: NotRequired[str | None]
    is_business_customer: NotRequired[bool]
    external_customer_id: NotRequired[str | None]
    customer_name: NotRequired[str | None]
    customer_email: NotRequired[str | None]
    customer_ip_address: NotRequired[str | None]
    customer_billing_name: NotRequired[str | None]
    customer_billing_address: NotRequired[AddressInput | None]
    customer_tax_id: NotRequired[str | None]
    customer_metadata: NotRequired[dict[str, Any]]
    subscription_id: NotRequired[str | None]
    success_url: NotRequired[str | None]
    return_url: NotRequired[str | None]
    embed_origin: NotRequired[str | None]
    locale: NotRequired[str | None]
    currency: NotRequired[PresentmentCurrency | None]
    product_id: str

class CheckoutProductsCreate(TypedDict):
    """Create a new checkout session from a list of products.
Customers will be able to switch between those products.

Metadata set on the checkout will be copied
to the resulting order and/or subscription."""
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    metadata: NotRequired[dict[str, Any]]
    custom_field_data: NotRequired[dict[str, Any]]
    discount_id: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool]
    require_billing_address: NotRequired[bool]
    amount: NotRequired[int | None]
    seats: NotRequired[int | None]
    allow_trial: NotRequired[bool]
    customer_id: NotRequired[str | None]
    is_business_customer: NotRequired[bool]
    external_customer_id: NotRequired[str | None]
    customer_name: NotRequired[str | None]
    customer_email: NotRequired[str | None]
    customer_ip_address: NotRequired[str | None]
    customer_billing_name: NotRequired[str | None]
    customer_billing_address: NotRequired[AddressInput | None]
    customer_tax_id: NotRequired[str | None]
    customer_metadata: NotRequired[dict[str, Any]]
    subscription_id: NotRequired[str | None]
    success_url: NotRequired[str | None]
    return_url: NotRequired[str | None]
    embed_origin: NotRequired[str | None]
    locale: NotRequired[str | None]
    currency: NotRequired[PresentmentCurrency | None]
    products: list[str]
    prices: NotRequired[dict[str, Any] | None]

class CheckoutPublic(TypedDict):
    """Checkout session data retrieved using the client secret."""
    id: str
    created_at: str
    modified_at: str | None
    custom_field_data: NotRequired[dict[str, Any]]
    payment_processor: PaymentProcessor
    status: CheckoutStatus
    client_secret: str
    url: str
    expires_at: str
    success_url: str
    return_url: str | None
    embed_origin: str | None
    amount: int
    seats: NotRequired[int | None]
    price_per_seat: NotRequired[int | None]
    discount_amount: int
    net_amount: int
    tax_amount: int | None
    total_amount: int
    currency: str
    allow_trial: bool | None
    active_trial_interval: TrialInterval | None
    active_trial_interval_count: int | None
    trial_end: str | None
    organization_id: str
    product_id: str | None
    product_price_id: str | None
    discount_id: str | None
    allow_discount_codes: bool
    require_billing_address: bool
    is_discount_applicable: bool
    is_free_product_price: bool
    is_payment_required: bool
    is_payment_setup_required: bool
    is_payment_form_required: bool
    customer_id: str | None
    is_business_customer: bool
    customer_name: str | None
    customer_email: str | None
    customer_ip_address: str | None
    customer_billing_name: str | None
    customer_billing_address: Address | None
    customer_tax_id: str | None
    locale: NotRequired[str | None]
    payment_processor_metadata: dict[str, Any]
    billing_address_fields: CheckoutBillingAddressFields
    products: list[CheckoutProduct]
    product: CheckoutProduct | None
    product_price: LegacyRecurringProductPrice | ProductPrice | None
    prices: dict[str, Any] | None
    discount: CheckoutDiscountFixedOnceForeverDuration | CheckoutDiscountFixedRepeatDuration | CheckoutDiscountPercentageOnceForeverDuration | CheckoutDiscountPercentageRepeatDuration | None
    organization: CheckoutOrganization
    attached_custom_fields: list[AttachedCustomField] | None

class CheckoutPublicConfirmed(TypedDict):
    """Checkout session data retrieved using the client secret after confirmation.

It contains a customer session token to retrieve order information
right after the checkout."""
    id: str
    created_at: str
    modified_at: str | None
    custom_field_data: NotRequired[dict[str, Any]]
    payment_processor: PaymentProcessor
    status: Literal['confirmed']
    client_secret: str
    url: str
    expires_at: str
    success_url: str
    return_url: str | None
    embed_origin: str | None
    amount: int
    seats: NotRequired[int | None]
    price_per_seat: NotRequired[int | None]
    discount_amount: int
    net_amount: int
    tax_amount: int | None
    total_amount: int
    currency: str
    allow_trial: bool | None
    active_trial_interval: TrialInterval | None
    active_trial_interval_count: int | None
    trial_end: str | None
    organization_id: str
    product_id: str | None
    product_price_id: str | None
    discount_id: str | None
    allow_discount_codes: bool
    require_billing_address: bool
    is_discount_applicable: bool
    is_free_product_price: bool
    is_payment_required: bool
    is_payment_setup_required: bool
    is_payment_form_required: bool
    customer_id: str | None
    is_business_customer: bool
    customer_name: str | None
    customer_email: str | None
    customer_ip_address: str | None
    customer_billing_name: str | None
    customer_billing_address: Address | None
    customer_tax_id: str | None
    locale: NotRequired[str | None]
    payment_processor_metadata: dict[str, Any]
    billing_address_fields: CheckoutBillingAddressFields
    products: list[CheckoutProduct]
    product: CheckoutProduct | None
    product_price: LegacyRecurringProductPrice | ProductPrice | None
    prices: dict[str, Any] | None
    discount: CheckoutDiscountFixedOnceForeverDuration | CheckoutDiscountFixedRepeatDuration | CheckoutDiscountPercentageOnceForeverDuration | CheckoutDiscountPercentageRepeatDuration | None
    organization: CheckoutOrganization
    attached_custom_fields: list[AttachedCustomField] | None
    customer_session_token: str

class CheckoutUpdate(TypedDict):
    """Update an existing checkout session using an access token."""
    custom_field_data: NotRequired[dict[str, Any]]
    product_id: NotRequired[str | None]
    product_price_id: NotRequired[str | None]
    amount: NotRequired[int | None]
    seats: NotRequired[int | None]
    is_business_customer: NotRequired[bool | None]
    customer_name: NotRequired[str | None]
    customer_email: NotRequired[str | None]
    customer_billing_name: NotRequired[str | None]
    customer_billing_address: NotRequired[AddressInput | None]
    customer_tax_id: NotRequired[str | None]
    locale: NotRequired[str | None]
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    metadata: NotRequired[dict[str, Any]]
    currency: NotRequired[PresentmentCurrency | None]
    discount_id: NotRequired[str | None]
    allow_discount_codes: NotRequired[bool | None]
    require_billing_address: NotRequired[bool | None]
    allow_trial: NotRequired[bool | None]
    customer_ip_address: NotRequired[str | None]
    customer_metadata: NotRequired[dict[str, Any] | None]
    success_url: NotRequired[str | None]
    return_url: NotRequired[str | None]
    embed_origin: NotRequired[str | None]

class CheckoutUpdatePublic(TypedDict):
    """Update an existing checkout session using the client secret."""
    custom_field_data: NotRequired[dict[str, Any]]
    product_id: NotRequired[str | None]
    product_price_id: NotRequired[str | None]
    amount: NotRequired[int | None]
    seats: NotRequired[int | None]
    is_business_customer: NotRequired[bool | None]
    customer_name: NotRequired[str | None]
    customer_email: NotRequired[str | None]
    customer_billing_name: NotRequired[str | None]
    customer_billing_address: NotRequired[AddressInput | None]
    customer_tax_id: NotRequired[str | None]
    locale: NotRequired[str | None]
    discount_code: NotRequired[str | None]
    allow_trial: NotRequired[Literal[False] | None]

class CostMetadataInput(TypedDict):
    amount: float | str
    currency: str

class CostMetadataOutput(TypedDict):
    amount: str
    currency: str

class CountAggregation(TypedDict):
    func: NotRequired[Literal['count']]

class CursorPagination(TypedDict):
    has_next_page: bool

class CustomFieldCheckbox(TypedDict):
    """Schema for a custom field of type checkbox."""
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    type: Literal['checkbox']
    slug: str
    name: str
    organization_id: str
    properties: CustomFieldCheckboxProperties

class CustomFieldCheckboxProperties(TypedDict):
    form_label: NotRequired[str]
    form_help_text: NotRequired[str]
    form_placeholder: NotRequired[str]

class CustomFieldCreateCheckbox(TypedDict):
    """Schema to create a custom field of type checkbox."""
    metadata: NotRequired[dict[str, Any]]
    type: Literal['checkbox']
    slug: str
    name: str
    organization_id: NotRequired[str | None]
    properties: CustomFieldCheckboxProperties

class CustomFieldCreateDate(TypedDict):
    """Schema to create a custom field of type date."""
    metadata: NotRequired[dict[str, Any]]
    type: Literal['date']
    slug: str
    name: str
    organization_id: NotRequired[str | None]
    properties: CustomFieldDateProperties

class CustomFieldCreateNumber(TypedDict):
    """Schema to create a custom field of type number."""
    metadata: NotRequired[dict[str, Any]]
    type: Literal['number']
    slug: str
    name: str
    organization_id: NotRequired[str | None]
    properties: CustomFieldNumberProperties

class CustomFieldCreateSelect(TypedDict):
    """Schema to create a custom field of type select."""
    metadata: NotRequired[dict[str, Any]]
    type: Literal['select']
    slug: str
    name: str
    organization_id: NotRequired[str | None]
    properties: CustomFieldSelectProperties

class CustomFieldCreateText(TypedDict):
    """Schema to create a custom field of type text."""
    metadata: NotRequired[dict[str, Any]]
    type: Literal['text']
    slug: str
    name: str
    organization_id: NotRequired[str | None]
    properties: CustomFieldTextProperties

class CustomFieldDate(TypedDict):
    """Schema for a custom field of type date."""
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    type: Literal['date']
    slug: str
    name: str
    organization_id: str
    properties: CustomFieldDateProperties

class CustomFieldDateProperties(TypedDict):
    form_label: NotRequired[str]
    form_help_text: NotRequired[str]
    form_placeholder: NotRequired[str]
    ge: NotRequired[int]
    le: NotRequired[int]

class CustomFieldNumber(TypedDict):
    """Schema for a custom field of type number."""
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    type: Literal['number']
    slug: str
    name: str
    organization_id: str
    properties: CustomFieldNumberProperties

class CustomFieldNumberProperties(TypedDict):
    form_label: NotRequired[str]
    form_help_text: NotRequired[str]
    form_placeholder: NotRequired[str]
    ge: NotRequired[int]
    le: NotRequired[int]

class CustomFieldSelect(TypedDict):
    """Schema for a custom field of type select."""
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    type: Literal['select']
    slug: str
    name: str
    organization_id: str
    properties: CustomFieldSelectProperties

class CustomFieldSelectOption(TypedDict):
    value: str
    label: str

class CustomFieldSelectProperties(TypedDict):
    form_label: NotRequired[str]
    form_help_text: NotRequired[str]
    form_placeholder: NotRequired[str]
    options: list[CustomFieldSelectOption]

class CustomFieldText(TypedDict):
    """Schema for a custom field of type text."""
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    type: Literal['text']
    slug: str
    name: str
    organization_id: str
    properties: CustomFieldTextProperties

class CustomFieldTextProperties(TypedDict):
    form_label: NotRequired[str]
    form_help_text: NotRequired[str]
    form_placeholder: NotRequired[str]
    textarea: NotRequired[bool]
    min_length: NotRequired[int]
    max_length: NotRequired[int]

class CustomFieldUpdateCheckbox(TypedDict):
    """Schema to update a custom field of type checkbox."""
    metadata: NotRequired[dict[str, Any]]
    name: NotRequired[str | None]
    slug: NotRequired[str | None]
    type: Literal['checkbox']
    properties: NotRequired[CustomFieldCheckboxProperties | None]

class CustomFieldUpdateDate(TypedDict):
    """Schema to update a custom field of type date."""
    metadata: NotRequired[dict[str, Any]]
    name: NotRequired[str | None]
    slug: NotRequired[str | None]
    type: Literal['date']
    properties: NotRequired[CustomFieldDateProperties | None]

class CustomFieldUpdateNumber(TypedDict):
    """Schema to update a custom field of type number."""
    metadata: NotRequired[dict[str, Any]]
    name: NotRequired[str | None]
    slug: NotRequired[str | None]
    type: Literal['number']
    properties: NotRequired[CustomFieldNumberProperties | None]

class CustomFieldUpdateSelect(TypedDict):
    """Schema to update a custom field of type select."""
    metadata: NotRequired[dict[str, Any]]
    name: NotRequired[str | None]
    slug: NotRequired[str | None]
    type: Literal['select']
    properties: NotRequired[CustomFieldSelectProperties | None]

class CustomFieldUpdateText(TypedDict):
    """Schema to update a custom field of type text."""
    metadata: NotRequired[dict[str, Any]]
    name: NotRequired[str | None]
    slug: NotRequired[str | None]
    type: Literal['text']
    properties: NotRequired[CustomFieldTextProperties | None]

class Customer(TypedDict):
    """A customer in an organization."""
    id: str
    created_at: str
    modified_at: str | None
    metadata: MetadataOutputType
    external_id: str | None
    email: str
    email_verified: bool
    type: NotRequired[CustomerType | None]
    name: str | None
    billing_address: Address | None
    tax_id: list[Any] | None
    locale: NotRequired[str | None]
    organization_id: str
    deleted_at: str | None
    avatar_url: str

class CustomerBenefitGrantCustom(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: str | None
    revoked_at: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    subscription_id: str | None
    order_id: str | None
    is_granted: bool
    is_revoked: bool
    error: NotRequired[BenefitGrantError | None]
    customer: CustomerPortalCustomer
    benefit: BenefitCustomSubscriber
    properties: BenefitGrantCustomProperties

class CustomerBenefitGrantCustomUpdate(TypedDict):
    benefit_type: Literal['custom']

class CustomerBenefitGrantDiscord(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: str | None
    revoked_at: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    subscription_id: str | None
    order_id: str | None
    is_granted: bool
    is_revoked: bool
    error: NotRequired[BenefitGrantError | None]
    customer: CustomerPortalCustomer
    benefit: BenefitDiscordSubscriber
    properties: BenefitGrantDiscordProperties

class CustomerBenefitGrantDiscordPropertiesUpdate(TypedDict):
    account_id: str | None

class CustomerBenefitGrantDiscordUpdate(TypedDict):
    benefit_type: Literal['discord']
    properties: CustomerBenefitGrantDiscordPropertiesUpdate

class CustomerBenefitGrantDownloadables(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: str | None
    revoked_at: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    subscription_id: str | None
    order_id: str | None
    is_granted: bool
    is_revoked: bool
    error: NotRequired[BenefitGrantError | None]
    customer: CustomerPortalCustomer
    benefit: BenefitDownloadablesSubscriber
    properties: BenefitGrantDownloadablesProperties

class CustomerBenefitGrantDownloadablesUpdate(TypedDict):
    benefit_type: Literal['downloadables']

class CustomerBenefitGrantGitHubRepository(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: str | None
    revoked_at: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    subscription_id: str | None
    order_id: str | None
    is_granted: bool
    is_revoked: bool
    error: NotRequired[BenefitGrantError | None]
    customer: CustomerPortalCustomer
    benefit: BenefitGitHubRepositorySubscriber
    properties: BenefitGrantGitHubRepositoryProperties

class CustomerBenefitGrantGitHubRepositoryPropertiesUpdate(TypedDict):
    account_id: str | None

class CustomerBenefitGrantGitHubRepositoryUpdate(TypedDict):
    benefit_type: Literal['github_repository']
    properties: CustomerBenefitGrantGitHubRepositoryPropertiesUpdate

class CustomerBenefitGrantLicenseKeys(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: str | None
    revoked_at: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    subscription_id: str | None
    order_id: str | None
    is_granted: bool
    is_revoked: bool
    error: NotRequired[BenefitGrantError | None]
    customer: CustomerPortalCustomer
    benefit: BenefitLicenseKeysSubscriber
    properties: BenefitGrantLicenseKeysProperties

class CustomerBenefitGrantLicenseKeysUpdate(TypedDict):
    benefit_type: Literal['license_keys']

class CustomerBenefitGrantMeterCredit(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    granted_at: str | None
    revoked_at: str | None
    customer_id: str
    member_id: NotRequired[str | None]
    benefit_id: str
    subscription_id: str | None
    order_id: str | None
    is_granted: bool
    is_revoked: bool
    error: NotRequired[BenefitGrantError | None]
    customer: CustomerPortalCustomer
    benefit: BenefitMeterCreditSubscriber
    properties: BenefitGrantMeterCreditProperties

class CustomerBenefitGrantMeterCreditUpdate(TypedDict):
    benefit_type: Literal['meter_credit']

class CustomerCreate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    external_id: NotRequired[str | None]
    email: str
    name: NotRequired[str | None]
    billing_address: NotRequired[AddressInput | None]
    tax_id: NotRequired[list[Any] | None]
    locale: NotRequired[str | None]
    type: NotRequired[CustomerType | None]
    organization_id: NotRequired[str | None]
    owner: NotRequired[OwnerCreate | None]

class CustomerCreatedEvent(TypedDict):
    """An event created by Polar when a customer is created."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['customer.created']
    metadata: CustomerCreatedMetadata

class CustomerCreatedMetadata(TypedDict):
    customer_id: str
    customer_email: str
    customer_name: str | None
    customer_external_id: str | None

class CustomerCustomerMeter(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    customer_id: str
    meter_id: str
    consumed_units: float
    credited_units: int
    balance: float
    meter: CustomerCustomerMeterMeter

class CustomerCustomerMeterMeter(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str

class CustomerCustomerSession(TypedDict):
    expires_at: str
    return_url: str | None

class CustomerDeletedEvent(TypedDict):
    """An event created by Polar when a customer is deleted."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['customer.deleted']
    metadata: CustomerDeletedMetadata

class CustomerDeletedMetadata(TypedDict):
    customer_id: str
    customer_email: str
    customer_name: str | None
    customer_external_id: str | None

class CustomerMeter(TypedDict):
    """An active customer meter, with current consumed and credited units."""
    id: str
    created_at: str
    modified_at: str | None
    customer_id: str
    meter_id: str
    consumed_units: float
    credited_units: int
    balance: float
    customer: Customer
    meter: Meter

class CustomerNotReady(TypedDict):
    error: Literal['CustomerNotReady']
    detail: str

class CustomerOrder(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    status: OrderStatus
    paid: bool
    subtotal_amount: int
    discount_amount: int
    net_amount: int
    tax_amount: int
    total_amount: int
    applied_balance_amount: int
    due_amount: int
    refunded_amount: int
    refunded_tax_amount: int
    currency: str
    billing_reason: OrderBillingReason
    billing_name: str | None
    billing_address: Address | None
    invoice_number: str
    is_invoice_generated: bool
    seats: NotRequired[int | None]
    customer_id: str
    product_id: str | None
    discount_id: str | None
    subscription_id: str | None
    checkout_id: str | None
    user_id: str
    product: CustomerOrderProduct | None
    subscription: CustomerOrderSubscription | None
    items: list[OrderItemSchema]
    description: str
    next_payment_attempt_at: NotRequired[str | None]

class CustomerOrderConfirmPayment(TypedDict):
    """Schema to confirm a retry payment using either a saved payment method or a new confirmation token."""
    confirmation_token_id: NotRequired[str | None]
    payment_method_id: NotRequired[str | None]
    payment_processor: NotRequired[PaymentProcessor]

class CustomerOrderInvoice(TypedDict):
    """Order's invoice data."""
    url: str

class CustomerOrderPaymentConfirmation(TypedDict):
    """Response after confirming a retry payment."""
    status: str
    client_secret: NotRequired[str | None]
    error: NotRequired[str | None]

class CustomerOrderPaymentStatus(TypedDict):
    """Payment status for an order."""
    status: str
    error: NotRequired[str | None]

class CustomerOrderProduct(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    benefits: list[BenefitPublic]
    medias: list[ProductMediaFileRead]
    organization: CustomerOrganization

class CustomerOrderSubscription(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    amount: int
    currency: str
    recurring_interval: SubscriptionRecurringInterval
    recurring_interval_count: int
    status: SubscriptionStatus
    current_period_start: str
    current_period_end: str | None
    trial_start: str | None
    trial_end: str | None
    cancel_at_period_end: bool
    canceled_at: str | None
    started_at: str | None
    ends_at: str | None
    ended_at: str | None
    customer_id: str
    product_id: str
    discount_id: str | None
    checkout_id: str | None
    seats: NotRequired[int | None]
    customer_cancellation_reason: CustomerCancellationReason | None
    customer_cancellation_comment: str | None

class CustomerOrderUpdate(TypedDict):
    """Schema to update an order."""
    billing_name: NotRequired[str | None]
    billing_address: NotRequired[AddressInput | None]

class CustomerOrganization(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str
    slug: str
    avatar_url: str | None
    proration_behavior: SubscriptionProrationBehavior
    allow_customer_updates: bool
    customer_portal_settings: OrganizationCustomerPortalSettings
    organization_features: NotRequired[CustomerOrganizationFeatureSettings]

class CustomerOrganizationData(TypedDict):
    """Schema of an organization and related data for customer portal."""
    organization: CustomerOrganization
    products: list[CustomerProduct]

class CustomerOrganizationFeatureSettings(TypedDict):
    """Feature flags exposed to the customer portal."""
    member_model_enabled: NotRequired[bool]

class CustomerPaymentMethodConfirm(TypedDict):
    setup_intent_id: str
    set_default: bool

class CustomerPaymentMethodCreate(TypedDict):
    confirmation_token_id: str
    set_default: bool
    return_url: str

class CustomerPaymentMethodCreateRequiresActionResponse(TypedDict):
    status: Literal['requires_action']
    client_secret: str

class CustomerPaymentMethodCreateSucceededResponse(TypedDict):
    status: Literal['succeeded']
    payment_method: CustomerPaymentMethod

class CustomerPortalCustomer(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    email: str
    email_verified: bool
    name: str | None
    billing_name: str | None
    billing_address: Address | None
    tax_id: list[Any] | None
    oauth_accounts: dict[str, Any]
    default_payment_method_id: NotRequired[str | None]
    type: NotRequired[CustomerType | None]

class CustomerPortalCustomerUpdate(TypedDict):
    billing_name: NotRequired[str | None]
    billing_address: NotRequired[AddressInput | None]
    tax_id: NotRequired[str | None]

class CustomerPortalMember(TypedDict):
    """A member of the customer's team as seen in the customer portal."""
    created_at: str
    modified_at: str | None
    id: str
    email: str
    name: str | None
    role: MemberRole

class CustomerPortalMemberCreate(TypedDict):
    """Schema for adding a new member to the customer's team."""
    email: str
    name: NotRequired[str | None]
    role: NotRequired[MemberRole]

class CustomerPortalMemberUpdate(TypedDict):
    """Schema for updating a member's role in the customer portal."""
    role: NotRequired[MemberRole | None]

class CustomerPortalOAuthAccount(TypedDict):
    account_id: str
    account_username: str | None

class CustomerPortalSubscriptionSettings(TypedDict):
    update_seats: bool
    update_plan: bool

class CustomerPortalUsageSettings(TypedDict):
    show: bool

class CustomerProduct(TypedDict):
    """Schema of a product for customer portal."""
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    benefits: list[BenefitPublic]
    medias: list[ProductMediaFileRead]

class CustomerSeat(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    subscription_id: NotRequired[str | None]
    order_id: NotRequired[str | None]
    status: SeatStatus
    customer_id: NotRequired[str | None]
    member_id: NotRequired[str | None]
    member: NotRequired[Member | None]
    email: NotRequired[str | None]
    customer_email: NotRequired[str | None]
    invitation_token_expires_at: NotRequired[str | None]
    claimed_at: NotRequired[str | None]
    revoked_at: NotRequired[str | None]
    seat_metadata: NotRequired[dict[str, Any] | None]

class CustomerSeatClaimResponse(TypedDict):
    """Response after successfully claiming a seat."""
    seat: CustomerSeat
    customer_session_token: str

class CustomerSession(TypedDict):
    """A customer session that can be used to authenticate as a customer."""
    created_at: str
    modified_at: str | None
    id: str
    token: str
    expires_at: str
    return_url: str | None
    customer_portal_url: str
    customer_id: str
    customer: Customer

class CustomerSessionCustomerExternalIDCreate(TypedDict):
    """Schema for creating a customer session using an external customer ID."""
    return_url: NotRequired[str | None]
    external_customer_id: str

class CustomerSessionCustomerIDCreate(TypedDict):
    """Schema for creating a customer session using a customer ID."""
    return_url: NotRequired[str | None]
    customer_id: str

class CustomerState(TypedDict):
    """A customer along with additional state information:

* Active subscriptions
* Granted benefits
* Active meters"""
    id: str
    created_at: str
    modified_at: str | None
    metadata: MetadataOutputType
    external_id: str | None
    email: str
    email_verified: bool
    type: NotRequired[CustomerType | None]
    name: str | None
    billing_address: Address | None
    tax_id: list[Any] | None
    locale: NotRequired[str | None]
    organization_id: str
    deleted_at: str | None
    active_subscriptions: list[CustomerStateSubscription]
    granted_benefits: list[CustomerStateBenefitGrant]
    active_meters: list[CustomerStateMeter]
    avatar_url: str

class CustomerStateBenefitGrant(TypedDict):
    """An active benefit grant for a customer."""
    id: str
    created_at: str
    modified_at: str | None
    granted_at: str
    benefit_id: str
    benefit_type: BenefitType
    benefit_metadata: MetadataOutputType
    properties: BenefitGrantDiscordProperties | BenefitGrantGitHubRepositoryProperties | BenefitGrantDownloadablesProperties | BenefitGrantLicenseKeysProperties | BenefitGrantCustomProperties

class CustomerStateMeter(TypedDict):
    """An active meter for a customer, with latest consumed and credited units."""
    id: str
    created_at: str
    modified_at: str | None
    meter_id: str
    consumed_units: float
    credited_units: int
    balance: float

class CustomerStateSubscription(TypedDict):
    """An active customer subscription."""
    id: str
    created_at: str
    modified_at: str | None
    custom_field_data: NotRequired[dict[str, Any]]
    metadata: MetadataOutputType
    status: Literal['active', 'trialing']
    amount: int
    currency: str
    recurring_interval: SubscriptionRecurringInterval
    current_period_start: str
    current_period_end: str | None
    trial_start: str | None
    trial_end: str | None
    cancel_at_period_end: bool
    canceled_at: str | None
    started_at: str | None
    ends_at: str | None
    product_id: str
    discount_id: str | None
    meters: list[CustomerStateSubscriptionMeter]

class CustomerStateSubscriptionMeter(TypedDict):
    """Current consumption and spending for a subscription meter."""
    created_at: str
    modified_at: str | None
    id: str
    consumed_units: float
    credited_units: int
    amount: int
    meter_id: str

class CustomerSubscription(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    amount: int
    currency: str
    recurring_interval: SubscriptionRecurringInterval
    recurring_interval_count: int
    status: SubscriptionStatus
    current_period_start: str
    current_period_end: str | None
    trial_start: str | None
    trial_end: str | None
    cancel_at_period_end: bool
    canceled_at: str | None
    started_at: str | None
    ends_at: str | None
    ended_at: str | None
    customer_id: str
    product_id: str
    discount_id: str | None
    checkout_id: str | None
    seats: NotRequired[int | None]
    customer_cancellation_reason: CustomerCancellationReason | None
    customer_cancellation_comment: str | None
    product: CustomerSubscriptionProduct
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    meters: list[CustomerSubscriptionMeter]

class CustomerSubscriptionCancel(TypedDict):
    cancel_at_period_end: NotRequired[bool | None]
    cancellation_reason: NotRequired[CustomerCancellationReason | None]
    cancellation_comment: NotRequired[str | None]

class CustomerSubscriptionMeter(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    consumed_units: float
    credited_units: int
    amount: int
    meter_id: str
    meter: CustomerSubscriptionMeterMeter

class CustomerSubscriptionMeterMeter(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str

class CustomerSubscriptionProduct(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    benefits: list[BenefitPublic]
    medias: list[ProductMediaFileRead]
    organization: CustomerOrganization

class CustomerSubscriptionUpdateProduct(TypedDict):
    product_id: str

class CustomerSubscriptionUpdateSeats(TypedDict):
    seats: int
    proration_behavior: NotRequired[SubscriptionProrationBehavior | None]

class CustomerUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    email: NotRequired[str | None]
    name: NotRequired[str | None]
    billing_address: NotRequired[AddressInput | None]
    tax_id: NotRequired[list[Any] | None]
    locale: NotRequired[str | None]
    external_id: NotRequired[str | None]
    type: NotRequired[CustomerType | None]

class CustomerUpdateExternalID(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    email: NotRequired[str | None]
    name: NotRequired[str | None]
    billing_address: NotRequired[AddressInput | None]
    tax_id: NotRequired[list[Any] | None]
    locale: NotRequired[str | None]

class CustomerUpdatedEvent(TypedDict):
    """An event created by Polar when a customer is updated."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['customer.updated']
    metadata: CustomerUpdatedMetadata

class CustomerUpdatedFields(TypedDict):
    name: NotRequired[str | None]
    email: NotRequired[str | None]
    billing_address: NotRequired[AddressDict | None]
    tax_id: NotRequired[str | None]
    metadata: NotRequired[dict[str, Any] | None]

class CustomerUpdatedMetadata(TypedDict):
    customer_id: str
    customer_email: str
    customer_name: str | None
    customer_external_id: str | None
    updated_fields: CustomerUpdatedFields

class CustomerWallet(TypedDict):
    """A wallet represents your balance with an organization.

You can top-up your wallet and use the balance to pay for usage."""
    id: str
    created_at: str
    modified_at: str | None
    customer_id: str
    balance: int
    currency: str

class CustomerWithMembers(TypedDict):
    """A customer in an organization with their members loaded."""
    id: str
    created_at: str
    modified_at: str | None
    metadata: MetadataOutputType
    external_id: str | None
    email: str
    email_verified: bool
    type: NotRequired[CustomerType | None]
    name: str | None
    billing_address: Address | None
    tax_id: list[Any] | None
    locale: NotRequired[str | None]
    organization_id: str
    deleted_at: str | None
    members: NotRequired[list[Member]]
    avatar_url: str

class DiscountFixedOnceForeverDuration(TypedDict):
    """Schema for a fixed amount discount that is applied once or forever."""
    duration: DiscountDuration
    type: DiscountType
    amount: int
    currency: str
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str
    products: list[DiscountProduct]

class DiscountFixedOnceForeverDurationBase(TypedDict):
    duration: DiscountDuration
    type: DiscountType
    amount: int
    currency: str
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str

class DiscountFixedOnceForeverDurationCreate(TypedDict):
    """Schema to create a fixed amount discount that is applied once or forever."""
    duration: DiscountDuration
    type: DiscountType
    amount: int
    currency: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]
    name: str
    code: NotRequired[str | None]
    starts_at: NotRequired[str | None]
    ends_at: NotRequired[str | None]
    max_redemptions: NotRequired[int | None]
    products: NotRequired[list[str] | None]
    organization_id: NotRequired[str | None]

class DiscountFixedRepeatDuration(TypedDict):
    """Schema for a fixed amount discount that is applied on every invoice
for a certain number of months."""
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    amount: int
    currency: str
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str
    products: list[DiscountProduct]

class DiscountFixedRepeatDurationBase(TypedDict):
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    amount: int
    currency: str
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str

class DiscountFixedRepeatDurationCreate(TypedDict):
    """Schema to create a fixed amount discount that is applied on every invoice
for a certain number of months."""
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    amount: int
    currency: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]
    name: str
    code: NotRequired[str | None]
    starts_at: NotRequired[str | None]
    ends_at: NotRequired[str | None]
    max_redemptions: NotRequired[int | None]
    products: NotRequired[list[str] | None]
    organization_id: NotRequired[str | None]

class DiscountPercentageOnceForeverDuration(TypedDict):
    """Schema for a percentage discount that is applied once or forever."""
    duration: DiscountDuration
    type: DiscountType
    basis_points: int
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str
    products: list[DiscountProduct]

class DiscountPercentageOnceForeverDurationBase(TypedDict):
    duration: DiscountDuration
    type: DiscountType
    basis_points: int
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str

class DiscountPercentageOnceForeverDurationCreate(TypedDict):
    """Schema to create a percentage discount that is applied once or forever."""
    duration: DiscountDuration
    type: DiscountType
    basis_points: int
    metadata: NotRequired[dict[str, Any]]
    name: str
    code: NotRequired[str | None]
    starts_at: NotRequired[str | None]
    ends_at: NotRequired[str | None]
    max_redemptions: NotRequired[int | None]
    products: NotRequired[list[str] | None]
    organization_id: NotRequired[str | None]

class DiscountPercentageRepeatDuration(TypedDict):
    """Schema for a percentage discount that is applied on every invoice
for a certain number of months."""
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    basis_points: int
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str
    products: list[DiscountProduct]

class DiscountPercentageRepeatDurationBase(TypedDict):
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    basis_points: int
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    name: str
    code: str | None
    starts_at: str | None
    ends_at: str | None
    max_redemptions: int | None
    redemptions_count: int
    organization_id: str

class DiscountPercentageRepeatDurationCreate(TypedDict):
    """Schema to create a percentage discount that is applied on every invoice
for a certain number of months."""
    duration: DiscountDuration
    duration_in_months: int
    type: DiscountType
    basis_points: int
    metadata: NotRequired[dict[str, Any]]
    name: str
    code: NotRequired[str | None]
    starts_at: NotRequired[str | None]
    ends_at: NotRequired[str | None]
    max_redemptions: NotRequired[int | None]
    products: NotRequired[list[str] | None]
    organization_id: NotRequired[str | None]

class DiscountProduct(TypedDict):
    """A product that a discount can be applied to."""
    metadata: MetadataOutputType
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str

class DiscountUpdate(TypedDict):
    """Schema to update a discount."""
    metadata: NotRequired[dict[str, Any]]
    name: NotRequired[str | None]
    code: NotRequired[str | None]
    starts_at: NotRequired[str | None]
    ends_at: NotRequired[str | None]
    max_redemptions: NotRequired[int | None]
    duration: NotRequired[DiscountDuration | None]
    duration_in_months: NotRequired[int | None]
    type: NotRequired[DiscountType | None]
    amount: NotRequired[int | None]
    currency: NotRequired[str | None]
    basis_points: NotRequired[int | None]
    products: NotRequired[list[str] | None]

class Dispute(TypedDict):
    """Schema representing a dispute.

A dispute is a challenge raised by a customer or their bank regarding a payment."""
    created_at: str
    modified_at: str | None
    id: str
    status: DisputeStatus
    resolved: bool
    closed: bool
    amount: int
    tax_amount: int
    currency: str
    order_id: str
    payment_id: str

class DownloadableFileCreate(TypedDict):
    """Schema to create a file to be associated with the downloadables benefit."""
    organization_id: NotRequired[str | None]
    name: str
    mime_type: str
    size: int
    checksum_sha256_base64: NotRequired[str | None]
    upload: S3FileCreateMultipart
    service: Literal['downloadable']
    version: NotRequired[str | None]

class DownloadableFileRead(TypedDict):
    """File to be associated with the downloadables benefit."""
    id: str
    organization_id: str
    name: str
    path: str
    mime_type: str
    size: int
    storage_version: str | None
    checksum_etag: str | None
    checksum_sha256_base64: str | None
    checksum_sha256_hex: str | None
    last_modified_at: str | None
    version: str | None
    service: Literal['downloadable']
    is_uploaded: bool
    created_at: str
    size_readable: str

class DownloadableRead(TypedDict):
    id: str
    benefit_id: str
    file: FileDownload

class EventCreateCustomer(TypedDict):
    timestamp: NotRequired[str]
    name: str
    organization_id: NotRequired[str | None]
    external_id: NotRequired[str | None]
    parent_id: NotRequired[str | None]
    metadata: NotRequired[EventMetadataInput]
    customer_id: str
    member_id: NotRequired[str | None]

class EventCreateExternalCustomer(TypedDict):
    timestamp: NotRequired[str]
    name: str
    organization_id: NotRequired[str | None]
    external_id: NotRequired[str | None]
    parent_id: NotRequired[str | None]
    metadata: NotRequired[EventMetadataInput]
    external_customer_id: str
    external_member_id: NotRequired[str | None]

class EventMetadataInput(TypedDict):
    _cost: NotRequired[CostMetadataInput]
    _llm: NotRequired[LLMMetadata]

class EventMetadataOutput(TypedDict):
    _cost: NotRequired[CostMetadataOutput]
    _llm: NotRequired[LLMMetadata]

class EventName(TypedDict):
    name: str
    source: EventSource
    occurrences: int
    first_seen: str
    last_seen: str

class EventType(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str
    label: str
    label_property_selector: NotRequired[str | None]
    organization_id: str

class EventTypeUpdate(TypedDict):
    label: str
    label_property_selector: NotRequired[str | None]

class EventTypeWithStats(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str
    label: str
    label_property_selector: NotRequired[str | None]
    organization_id: str
    source: EventSource
    occurrences: int
    first_seen: str
    last_seen: str

class EventsIngest(TypedDict):
    events: list[EventCreateCustomer | EventCreateExternalCustomer]

class EventsIngestResponse(TypedDict):
    inserted: int
    duplicates: NotRequired[int]

class ExistingProductPrice(TypedDict):
    """A price that already exists for this product.

Useful when updating a product if you want to keep an existing price."""
    id: str

class ExpiredCheckoutError(TypedDict):
    error: Literal['ExpiredCheckoutError']
    detail: str

class FileDownload(TypedDict):
    id: str
    organization_id: str
    name: str
    path: str
    mime_type: str
    size: int
    storage_version: str | None
    checksum_etag: str | None
    checksum_sha256_base64: str | None
    checksum_sha256_hex: str | None
    last_modified_at: str | None
    download: S3DownloadURL
    version: str | None
    is_uploaded: bool
    service: FileServiceTypes
    size_readable: str

class FilePatch(TypedDict):
    name: NotRequired[str | None]
    version: NotRequired[str | None]

class FileUpload(TypedDict):
    id: str
    organization_id: str
    name: str
    path: str
    mime_type: str
    size: int
    storage_version: str | None
    checksum_etag: str | None
    checksum_sha256_base64: str | None
    checksum_sha256_hex: str | None
    last_modified_at: str | None
    upload: S3FileUploadMultipart
    version: str | None
    is_uploaded: NotRequired[bool]
    service: FileServiceTypes
    size_readable: str

class FileUploadCompleted(TypedDict):
    id: str
    path: str
    parts: list[S3FileUploadCompletedPart]

class Filter(TypedDict):
    conjunction: FilterConjunction
    clauses: list[FilterClause | Filter]

class FilterClause(TypedDict):
    property: str
    operator: FilterOperator
    value: str | int | bool

class GenericPayment(TypedDict):
    """Schema of a payment with a generic payment method."""
    created_at: str
    modified_at: str | None
    id: str
    processor: PaymentProcessor
    status: PaymentStatus
    amount: int
    currency: str
    method: str
    decline_reason: str | None
    decline_message: str | None
    organization_id: str
    checkout_id: str | None
    order_id: str | None
    processor_metadata: NotRequired[dict[str, Any]]

class HTTPValidationError(TypedDict):
    detail: NotRequired[list[ValidationError]]

class IntrospectTokenResponse(TypedDict):
    active: bool
    client_id: str
    token_type: Literal['access_token', 'refresh_token']
    scope: str
    sub_type: SubType
    sub: str
    aud: str
    iss: str
    exp: int
    iat: int

class LLMMetadata(TypedDict):
    vendor: str
    model: str
    prompt: NotRequired[str | None]
    response: NotRequired[str | None]
    input_tokens: int
    cached_input_tokens: NotRequired[int]
    output_tokens: int
    total_tokens: int

class LegacyRecurringProductPriceCustom(TypedDict):
    """A pay-what-you-want recurring price for a product, i.e. a subscription.

**Deprecated**: The recurring interval should be set on the product itself."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['custom']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: Literal['recurring']
    recurring_interval: SubscriptionRecurringInterval
    minimum_amount: int
    maximum_amount: int | None
    preset_amount: int | None
    legacy: Literal[True]

class LegacyRecurringProductPriceFixed(TypedDict):
    """A recurring price for a product, i.e. a subscription.

**Deprecated**: The recurring interval should be set on the product itself."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['fixed']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: Literal['recurring']
    recurring_interval: SubscriptionRecurringInterval
    price_amount: int
    legacy: Literal[True]

class LegacyRecurringProductPriceFree(TypedDict):
    """A free recurring price for a product, i.e. a subscription.

**Deprecated**: The recurring interval should be set on the product itself."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['free']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: Literal['recurring']
    recurring_interval: SubscriptionRecurringInterval
    legacy: Literal[True]

class LicenseKeyActivate(TypedDict):
    key: str
    organization_id: str
    label: str
    conditions: NotRequired[dict[str, Any]]
    meta: NotRequired[dict[str, Any]]

class LicenseKeyActivationBase(TypedDict):
    id: str
    license_key_id: str
    label: str
    meta: dict[str, Any]
    created_at: str
    modified_at: str | None

class LicenseKeyActivationRead(TypedDict):
    id: str
    license_key_id: str
    label: str
    meta: dict[str, Any]
    created_at: str
    modified_at: str | None
    license_key: LicenseKeyRead

class LicenseKeyCustomer(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    metadata: MetadataOutputType
    external_id: str | None
    email: str
    email_verified: bool
    type: NotRequired[CustomerType | None]
    name: str | None
    billing_address: Address | None
    tax_id: list[Any] | None
    locale: NotRequired[str | None]
    organization_id: str
    deleted_at: str | None
    avatar_url: str

class LicenseKeyDeactivate(TypedDict):
    key: str
    organization_id: str
    activation_id: str

class LicenseKeyRead(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    organization_id: str
    customer_id: str
    customer: LicenseKeyCustomer
    benefit_id: str
    key: str
    display_key: str
    status: LicenseKeyStatus
    limit_activations: int | None
    usage: int
    limit_usage: int | None
    validations: int
    last_validated_at: str | None
    expires_at: str | None

class LicenseKeyUpdate(TypedDict):
    status: NotRequired[LicenseKeyStatus | None]
    usage: NotRequired[int]
    limit_activations: NotRequired[int | None]
    limit_usage: NotRequired[int | None]
    expires_at: NotRequired[str | None]

class LicenseKeyUser(TypedDict):
    id: str
    email: str
    public_name: str
    avatar_url: NotRequired[str | None]

class LicenseKeyValidate(TypedDict):
    key: str
    organization_id: str
    activation_id: NotRequired[str | None]
    benefit_id: NotRequired[str | None]
    customer_id: NotRequired[str | None]
    increment_usage: NotRequired[int | None]
    conditions: NotRequired[dict[str, Any]]

class LicenseKeyWithActivations(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    organization_id: str
    customer_id: str
    customer: LicenseKeyCustomer
    benefit_id: str
    key: str
    display_key: str
    status: LicenseKeyStatus
    limit_activations: int | None
    usage: int
    limit_usage: int | None
    validations: int
    last_validated_at: str | None
    expires_at: str | None
    activations: list[LicenseKeyActivationBase]

class ListResourceWithCursorPagination_Event_(TypedDict):
    items: list[Event]
    pagination: CursorPagination

class ListResource_BenefitGrant_(TypedDict):
    items: list[BenefitGrant]
    pagination: Pagination

class ListResource_Benefit_(TypedDict):
    items: list[Benefit]
    pagination: Pagination

class ListResource_CheckoutLink_(TypedDict):
    items: list[CheckoutLink]
    pagination: Pagination

class ListResource_Checkout_(TypedDict):
    items: list[Checkout]
    pagination: Pagination

class ListResource_CustomField_(TypedDict):
    items: list[CustomField]
    pagination: Pagination

class ListResource_CustomerBenefitGrant_(TypedDict):
    items: list[CustomerBenefitGrant]
    pagination: Pagination

class ListResource_CustomerCustomerMeter_(TypedDict):
    items: list[CustomerCustomerMeter]
    pagination: Pagination

class ListResource_CustomerMeter_(TypedDict):
    items: list[CustomerMeter]
    pagination: Pagination

class ListResource_CustomerOrder_(TypedDict):
    items: list[CustomerOrder]
    pagination: Pagination

class ListResource_CustomerPaymentMethod_(TypedDict):
    items: list[CustomerPaymentMethod]
    pagination: Pagination

class ListResource_CustomerSubscription_(TypedDict):
    items: list[CustomerSubscription]
    pagination: Pagination

class ListResource_CustomerWallet_(TypedDict):
    items: list[CustomerWallet]
    pagination: Pagination

class ListResource_CustomerWithMembers_(TypedDict):
    items: list[CustomerWithMembers]
    pagination: Pagination

class ListResource_Discount_(TypedDict):
    items: list[Discount]
    pagination: Pagination

class ListResource_Dispute_(TypedDict):
    items: list[Dispute]
    pagination: Pagination

class ListResource_DownloadableRead_(TypedDict):
    items: list[DownloadableRead]
    pagination: Pagination

class ListResource_EventName_(TypedDict):
    items: list[EventName]
    pagination: Pagination

class ListResource_EventTypeWithStats_(TypedDict):
    items: list[EventTypeWithStats]
    pagination: Pagination

class ListResource_Event_(TypedDict):
    items: list[Event]
    pagination: Pagination

class ListResource_FileRead_(TypedDict):
    items: list[DownloadableFileRead | ProductMediaFileRead | OrganizationAvatarFileRead]
    pagination: Pagination

class ListResource_LicenseKeyRead_(TypedDict):
    items: list[LicenseKeyRead]
    pagination: Pagination

class ListResource_Member_(TypedDict):
    items: list[Member]
    pagination: Pagination

class ListResource_Meter_(TypedDict):
    items: list[Meter]
    pagination: Pagination

class ListResource_Order_(TypedDict):
    items: list[Order]
    pagination: Pagination

class ListResource_OrganizationAccessToken_(TypedDict):
    items: list[OrganizationAccessToken]
    pagination: Pagination

class ListResource_Organization_(TypedDict):
    items: list[Organization]
    pagination: Pagination

class ListResource_Product_(TypedDict):
    items: list[Product]
    pagination: Pagination

class ListResource_Refund_(TypedDict):
    items: list[Refund]
    pagination: Pagination

class ListResource_Subscription_(TypedDict):
    items: list[Subscription]
    pagination: Pagination

class ListResource_WebhookDelivery_(TypedDict):
    items: list[WebhookDelivery]
    pagination: Pagination

class ListResource_WebhookEndpoint_(TypedDict):
    items: list[WebhookEndpoint]
    pagination: Pagination

class ListResource__(TypedDict):
    items: list[Payment]
    pagination: Pagination

class Member(TypedDict):
    """A member of a customer."""
    id: str
    created_at: str
    modified_at: str | None
    customer_id: str
    email: str
    name: str | None
    external_id: str | None
    role: MemberRole

class MemberCreate(TypedDict):
    """Schema for creating a new member."""
    customer_id: str
    email: str
    name: NotRequired[str | None]
    external_id: NotRequired[str | None]
    role: NotRequired[MemberRole]

class MemberSession(TypedDict):
    """A member session that can be used to authenticate as a member in the customer portal."""
    created_at: str
    modified_at: str | None
    id: str
    token: str
    expires_at: str
    return_url: str | None
    member_portal_url: str
    member_id: str
    member: Member
    customer_id: str
    customer: Customer

class MemberSessionCreate(TypedDict):
    """Schema for creating a member session using a member ID."""
    member_id: str
    return_url: NotRequired[str | None]

class MemberUpdate(TypedDict):
    """Schema for updating a member."""
    name: NotRequired[str | None]
    role: NotRequired[MemberRole | None]

class MetadataOutputType(TypedDict):
    pass

class Meter(TypedDict):
    metadata: MetadataOutputType
    created_at: str
    modified_at: str | None
    id: str
    name: str
    filter: Filter
    aggregation: CountAggregation | PropertyAggregation | UniqueAggregation
    organization_id: str
    archived_at: NotRequired[str | None]

class MeterCreate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    name: str
    filter: Filter
    aggregation: CountAggregation | PropertyAggregation | UniqueAggregation
    organization_id: NotRequired[str | None]

class MeterCreditEvent(TypedDict):
    """An event created by Polar when credits are added to a customer meter."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['meter.credited']
    metadata: MeterCreditedMetadata

class MeterCreditedMetadata(TypedDict):
    meter_id: str
    units: int
    rollover: bool

class MeterQuantities(TypedDict):
    quantities: list[MeterQuantity]
    total: float

class MeterQuantity(TypedDict):
    timestamp: str
    quantity: float

class MeterResetEvent(TypedDict):
    """An event created by Polar when a customer meter is reset."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['meter.reset']
    metadata: MeterResetMetadata

class MeterResetMetadata(TypedDict):
    meter_id: str

class MeterUpdate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    name: NotRequired[str | None]
    filter: NotRequired[Filter | None]
    aggregation: NotRequired[CountAggregation | PropertyAggregation | UniqueAggregation | None]
    is_archived: NotRequired[bool | None]

class Metric(TypedDict):
    """Information about a metric."""
    slug: str
    display_name: str
    type: MetricType

class MetricPeriod(TypedDict):
    timestamp: str
    orders: NotRequired[int | float | None]
    revenue: NotRequired[int | float | None]
    net_revenue: NotRequired[int | float | None]
    cumulative_revenue: NotRequired[int | float | None]
    net_cumulative_revenue: NotRequired[int | float | None]
    costs: NotRequired[int | float | None]
    cumulative_costs: NotRequired[int | float | None]
    average_order_value: NotRequired[int | float | None]
    net_average_order_value: NotRequired[int | float | None]
    average_revenue_per_user: NotRequired[int | float | None]
    cost_per_user: NotRequired[int | float | None]
    active_user_by_event: NotRequired[int | float | None]
    one_time_products: NotRequired[int | float | None]
    one_time_products_revenue: NotRequired[int | float | None]
    one_time_products_net_revenue: NotRequired[int | float | None]
    new_subscriptions: NotRequired[int | float | None]
    new_subscriptions_revenue: NotRequired[int | float | None]
    new_subscriptions_net_revenue: NotRequired[int | float | None]
    renewed_subscriptions: NotRequired[int | float | None]
    renewed_subscriptions_revenue: NotRequired[int | float | None]
    renewed_subscriptions_net_revenue: NotRequired[int | float | None]
    active_subscriptions: NotRequired[int | float | None]
    committed_subscriptions: NotRequired[int | float | None]
    monthly_recurring_revenue: NotRequired[int | float | None]
    committed_monthly_recurring_revenue: NotRequired[int | float | None]
    checkouts: NotRequired[int | float | None]
    succeeded_checkouts: NotRequired[int | float | None]
    checkouts_conversion: NotRequired[int | float | None]
    canceled_subscriptions: NotRequired[int | float | None]
    canceled_subscriptions_customer_service: NotRequired[int | float | None]
    canceled_subscriptions_low_quality: NotRequired[int | float | None]
    canceled_subscriptions_missing_features: NotRequired[int | float | None]
    canceled_subscriptions_switched_service: NotRequired[int | float | None]
    canceled_subscriptions_too_complex: NotRequired[int | float | None]
    canceled_subscriptions_too_expensive: NotRequired[int | float | None]
    canceled_subscriptions_unused: NotRequired[int | float | None]
    canceled_subscriptions_other: NotRequired[int | float | None]
    churned_subscriptions: NotRequired[int | float | None]
    churn_rate: NotRequired[int | float | None]
    ltv: NotRequired[int | float | None]
    gross_margin: NotRequired[int | float | None]
    gross_margin_percentage: NotRequired[int | float | None]
    cashflow: NotRequired[int | float | None]

class Metrics(TypedDict):
    orders: NotRequired[Metric | None]
    revenue: NotRequired[Metric | None]
    net_revenue: NotRequired[Metric | None]
    cumulative_revenue: NotRequired[Metric | None]
    net_cumulative_revenue: NotRequired[Metric | None]
    costs: NotRequired[Metric | None]
    cumulative_costs: NotRequired[Metric | None]
    average_order_value: NotRequired[Metric | None]
    net_average_order_value: NotRequired[Metric | None]
    average_revenue_per_user: NotRequired[Metric | None]
    cost_per_user: NotRequired[Metric | None]
    active_user_by_event: NotRequired[Metric | None]
    one_time_products: NotRequired[Metric | None]
    one_time_products_revenue: NotRequired[Metric | None]
    one_time_products_net_revenue: NotRequired[Metric | None]
    new_subscriptions: NotRequired[Metric | None]
    new_subscriptions_revenue: NotRequired[Metric | None]
    new_subscriptions_net_revenue: NotRequired[Metric | None]
    renewed_subscriptions: NotRequired[Metric | None]
    renewed_subscriptions_revenue: NotRequired[Metric | None]
    renewed_subscriptions_net_revenue: NotRequired[Metric | None]
    active_subscriptions: NotRequired[Metric | None]
    committed_subscriptions: NotRequired[Metric | None]
    monthly_recurring_revenue: NotRequired[Metric | None]
    committed_monthly_recurring_revenue: NotRequired[Metric | None]
    checkouts: NotRequired[Metric | None]
    succeeded_checkouts: NotRequired[Metric | None]
    checkouts_conversion: NotRequired[Metric | None]
    canceled_subscriptions: NotRequired[Metric | None]
    canceled_subscriptions_customer_service: NotRequired[Metric | None]
    canceled_subscriptions_low_quality: NotRequired[Metric | None]
    canceled_subscriptions_missing_features: NotRequired[Metric | None]
    canceled_subscriptions_switched_service: NotRequired[Metric | None]
    canceled_subscriptions_too_complex: NotRequired[Metric | None]
    canceled_subscriptions_too_expensive: NotRequired[Metric | None]
    canceled_subscriptions_unused: NotRequired[Metric | None]
    canceled_subscriptions_other: NotRequired[Metric | None]
    churned_subscriptions: NotRequired[Metric | None]
    churn_rate: NotRequired[Metric | None]
    ltv: NotRequired[Metric | None]
    gross_margin: NotRequired[Metric | None]
    gross_margin_percentage: NotRequired[Metric | None]
    cashflow: NotRequired[Metric | None]

class MetricsIntervalLimit(TypedDict):
    """Date interval limit to get metrics for a given interval."""
    min_days: int
    max_days: int

class MetricsIntervalsLimits(TypedDict):
    """Date interval limits to get metrics for each interval."""
    hour: MetricsIntervalLimit
    day: MetricsIntervalLimit
    week: MetricsIntervalLimit
    month: MetricsIntervalLimit
    year: MetricsIntervalLimit

class MetricsLimits(TypedDict):
    """Date limits to get metrics."""
    min_date: str
    intervals: MetricsIntervalsLimits

class MetricsResponse(TypedDict):
    """Metrics response schema."""
    periods: list[MetricPeriod]
    totals: MetricsTotals
    metrics: Metrics

class MetricsTotals(TypedDict):
    orders: NotRequired[int | float | None]
    revenue: NotRequired[int | float | None]
    net_revenue: NotRequired[int | float | None]
    cumulative_revenue: NotRequired[int | float | None]
    net_cumulative_revenue: NotRequired[int | float | None]
    costs: NotRequired[int | float | None]
    cumulative_costs: NotRequired[int | float | None]
    average_order_value: NotRequired[int | float | None]
    net_average_order_value: NotRequired[int | float | None]
    average_revenue_per_user: NotRequired[int | float | None]
    cost_per_user: NotRequired[int | float | None]
    active_user_by_event: NotRequired[int | float | None]
    one_time_products: NotRequired[int | float | None]
    one_time_products_revenue: NotRequired[int | float | None]
    one_time_products_net_revenue: NotRequired[int | float | None]
    new_subscriptions: NotRequired[int | float | None]
    new_subscriptions_revenue: NotRequired[int | float | None]
    new_subscriptions_net_revenue: NotRequired[int | float | None]
    renewed_subscriptions: NotRequired[int | float | None]
    renewed_subscriptions_revenue: NotRequired[int | float | None]
    renewed_subscriptions_net_revenue: NotRequired[int | float | None]
    active_subscriptions: NotRequired[int | float | None]
    committed_subscriptions: NotRequired[int | float | None]
    monthly_recurring_revenue: NotRequired[int | float | None]
    committed_monthly_recurring_revenue: NotRequired[int | float | None]
    checkouts: NotRequired[int | float | None]
    succeeded_checkouts: NotRequired[int | float | None]
    checkouts_conversion: NotRequired[int | float | None]
    canceled_subscriptions: NotRequired[int | float | None]
    canceled_subscriptions_customer_service: NotRequired[int | float | None]
    canceled_subscriptions_low_quality: NotRequired[int | float | None]
    canceled_subscriptions_missing_features: NotRequired[int | float | None]
    canceled_subscriptions_switched_service: NotRequired[int | float | None]
    canceled_subscriptions_too_complex: NotRequired[int | float | None]
    canceled_subscriptions_too_expensive: NotRequired[int | float | None]
    canceled_subscriptions_unused: NotRequired[int | float | None]
    canceled_subscriptions_other: NotRequired[int | float | None]
    churned_subscriptions: NotRequired[int | float | None]
    churn_rate: NotRequired[int | float | None]
    ltv: NotRequired[int | float | None]
    gross_margin: NotRequired[int | float | None]
    gross_margin_percentage: NotRequired[int | float | None]
    cashflow: NotRequired[int | float | None]

class MissingInvoiceBillingDetails(TypedDict):
    error: Literal['MissingInvoiceBillingDetails']
    detail: str

class NotOpenCheckout(TypedDict):
    error: Literal['NotOpenCheckout']
    detail: str

class NotPaidOrder(TypedDict):
    error: Literal['NotPaidOrder']
    detail: str

class NotPermitted(TypedDict):
    error: Literal['NotPermitted']
    detail: str

class OAuth2ClientConfiguration(TypedDict):
    redirect_uris: list[str]
    token_endpoint_auth_method: NotRequired[Literal['client_secret_basic', 'client_secret_post', 'none']]
    grant_types: NotRequired[list[Literal['authorization_code', 'refresh_token']]]
    response_types: NotRequired[list[Literal['code']]]
    scope: NotRequired[str]
    client_name: str
    client_uri: NotRequired[str | None]
    logo_uri: NotRequired[str | None]
    tos_uri: NotRequired[str | None]
    policy_uri: NotRequired[str | None]
    default_sub_type: NotRequired[SubType]

class OAuth2ClientConfigurationUpdate(TypedDict):
    redirect_uris: list[str]
    token_endpoint_auth_method: NotRequired[Literal['client_secret_basic', 'client_secret_post', 'none']]
    grant_types: NotRequired[list[Literal['authorization_code', 'refresh_token']]]
    response_types: NotRequired[list[Literal['code']]]
    scope: NotRequired[str]
    client_name: str
    client_uri: NotRequired[str | None]
    logo_uri: NotRequired[str | None]
    tos_uri: NotRequired[str | None]
    policy_uri: NotRequired[str | None]
    default_sub_type: NotRequired[SubType]
    client_id: str

class OAuth2ClientPublic(TypedDict):
    created_at: str
    modified_at: str | None
    client_id: str
    client_name: str | None
    client_uri: str | None
    logo_uri: str | None
    tos_uri: str | None
    policy_uri: str | None

class Order(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    status: OrderStatus
    paid: bool
    subtotal_amount: int
    discount_amount: int
    net_amount: int
    tax_amount: int
    total_amount: int
    applied_balance_amount: int
    due_amount: int
    refunded_amount: int
    refunded_tax_amount: int
    currency: str
    billing_reason: OrderBillingReason
    billing_name: str | None
    billing_address: Address | None
    invoice_number: str
    is_invoice_generated: bool
    seats: NotRequired[int | None]
    customer_id: str
    product_id: str | None
    discount_id: str | None
    subscription_id: str | None
    checkout_id: str | None
    metadata: MetadataOutputType
    custom_field_data: NotRequired[dict[str, Any]]
    platform_fee_amount: int
    platform_fee_currency: str | None
    customer: OrderCustomer
    user_id: str
    product: OrderProduct | None
    discount: DiscountFixedOnceForeverDurationBase | DiscountFixedRepeatDurationBase | DiscountPercentageOnceForeverDurationBase | DiscountPercentageRepeatDurationBase | None
    subscription: OrderSubscription | None
    items: list[OrderItemSchema]
    description: str

class OrderCustomer(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    metadata: MetadataOutputType
    external_id: str | None
    email: str
    email_verified: bool
    type: NotRequired[CustomerType | None]
    name: str | None
    billing_address: Address | None
    tax_id: list[Any] | None
    locale: NotRequired[str | None]
    organization_id: str
    deleted_at: str | None
    avatar_url: str

class OrderInvoice(TypedDict):
    """Order's invoice data."""
    url: str

class OrderItemSchema(TypedDict):
    """An order line item."""
    created_at: str
    modified_at: str | None
    id: str
    label: str
    amount: int
    tax_amount: int
    proration: bool
    product_price_id: str | None

class OrderNotEligibleForRetry(TypedDict):
    error: Literal['OrderNotEligibleForRetry']
    detail: str

class OrderPaidEvent(TypedDict):
    """An event created by Polar when an order is paid."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['order.paid']
    metadata: OrderPaidMetadata

class OrderPaidMetadata(TypedDict):
    order_id: str
    product_id: NotRequired[str]
    billing_type: NotRequired[str]
    amount: int
    currency: NotRequired[str]
    net_amount: NotRequired[int]
    tax_amount: NotRequired[int]
    applied_balance_amount: NotRequired[int]
    discount_amount: NotRequired[int]
    discount_id: NotRequired[str]
    platform_fee: NotRequired[int]
    subscription_id: NotRequired[str]
    recurring_interval: NotRequired[str]
    recurring_interval_count: NotRequired[int]

class OrderProduct(TypedDict):
    metadata: MetadataOutputType
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str

class OrderRefundedEvent(TypedDict):
    """An event created by Polar when an order is refunded."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['order.refunded']
    metadata: OrderRefundedMetadata

class OrderRefundedMetadata(TypedDict):
    order_id: str
    refunded_amount: int
    currency: str

class OrderSubscription(TypedDict):
    metadata: MetadataOutputType
    created_at: str
    modified_at: str | None
    id: str
    amount: int
    currency: str
    recurring_interval: SubscriptionRecurringInterval
    recurring_interval_count: int
    status: SubscriptionStatus
    current_period_start: str
    current_period_end: str | None
    trial_start: str | None
    trial_end: str | None
    cancel_at_period_end: bool
    canceled_at: str | None
    started_at: str | None
    ends_at: str | None
    ended_at: str | None
    customer_id: str
    product_id: str
    discount_id: str | None
    checkout_id: str | None
    seats: NotRequired[int | None]
    customer_cancellation_reason: CustomerCancellationReason | None
    customer_cancellation_comment: str | None

class OrderUpdate(TypedDict):
    """Schema to update an order."""
    billing_name: NotRequired[str | None]
    billing_address: NotRequired[AddressInput | None]

class OrderUser(TypedDict):
    id: str
    email: str
    public_name: str
    avatar_url: NotRequired[str | None]
    github_username: NotRequired[str | None]

class Organization(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    name: str
    slug: str
    avatar_url: str | None
    proration_behavior: SubscriptionProrationBehavior
    allow_customer_updates: bool
    email: str | None
    website: str | None
    socials: list[OrganizationSocialLink]
    status: OrganizationStatus
    details_submitted_at: str | None
    default_presentment_currency: PresentmentCurrency
    feature_settings: OrganizationFeatureSettings | None
    subscription_settings: OrganizationSubscriptionSettings
    notification_settings: OrganizationNotificationSettings
    customer_email_settings: OrganizationCustomerEmailSettings
    customer_portal_settings: OrganizationCustomerPortalSettings

class OrganizationAccessToken(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    scopes: list[Scope]
    expires_at: str | None
    comment: str
    last_used_at: str | None
    organization_id: str

class OrganizationAccessTokenCreate(TypedDict):
    organization_id: NotRequired[str | None]
    comment: str
    expires_in: NotRequired[str | None]
    scopes: list[AvailableScope]

class OrganizationAccessTokenCreateResponse(TypedDict):
    organization_access_token: OrganizationAccessToken
    token: str

class OrganizationAccessTokenUpdate(TypedDict):
    comment: NotRequired[str | None]
    scopes: NotRequired[list[AvailableScope] | None]

class OrganizationAvatarFileCreate(TypedDict):
    """Schema to create a file to be used as an organization avatar."""
    organization_id: NotRequired[str | None]
    name: str
    mime_type: str
    size: int
    checksum_sha256_base64: NotRequired[str | None]
    upload: S3FileCreateMultipart
    service: Literal['organization_avatar']
    version: NotRequired[str | None]

class OrganizationAvatarFileRead(TypedDict):
    """File to be used as an organization avatar."""
    id: str
    organization_id: str
    name: str
    path: str
    mime_type: str
    size: int
    storage_version: str | None
    checksum_etag: str | None
    checksum_sha256_base64: str | None
    checksum_sha256_hex: str | None
    last_modified_at: str | None
    version: str | None
    service: Literal['organization_avatar']
    is_uploaded: bool
    created_at: str
    size_readable: str
    public_url: str

class OrganizationCreate(TypedDict):
    name: str
    slug: str
    avatar_url: NotRequired[str | None]
    email: NotRequired[str | None]
    website: NotRequired[str | None]
    socials: NotRequired[list[OrganizationSocialLink] | None]
    details: NotRequired[OrganizationDetails | None]
    feature_settings: NotRequired[OrganizationFeatureSettings | None]
    subscription_settings: NotRequired[OrganizationSubscriptionSettings | None]
    notification_settings: NotRequired[OrganizationNotificationSettings | None]
    customer_email_settings: NotRequired[OrganizationCustomerEmailSettings | None]
    customer_portal_settings: NotRequired[OrganizationCustomerPortalSettings | None]
    default_presentment_currency: NotRequired[PresentmentCurrency]

class OrganizationCustomerEmailSettings(TypedDict):
    order_confirmation: bool
    subscription_cancellation: bool
    subscription_confirmation: bool
    subscription_cycled: bool
    subscription_past_due: bool
    subscription_revoked: bool
    subscription_uncanceled: bool
    subscription_updated: bool

class OrganizationCustomerPortalSettings(TypedDict):
    usage: CustomerPortalUsageSettings
    subscription: CustomerPortalSubscriptionSettings

class OrganizationDetails(TypedDict):
    about: str
    product_description: str
    intended_use: str
    customer_acquisition: list[str]
    future_annual_revenue: int
    switching: NotRequired[bool]
    switching_from: NotRequired[Literal['paddle', 'lemon_squeezy', 'gumroad', 'stripe', 'other'] | None]
    previous_annual_revenue: NotRequired[int]

class OrganizationFeatureSettings(TypedDict):
    issue_funding_enabled: NotRequired[bool]
    seat_based_pricing_enabled: NotRequired[bool]
    revops_enabled: NotRequired[bool]
    wallets_enabled: NotRequired[bool]
    member_model_enabled: NotRequired[bool]
    tinybird_read: NotRequired[bool]
    tinybird_compare: NotRequired[bool]
    presentment_currencies_enabled: NotRequired[bool]

class OrganizationNotificationSettings(TypedDict):
    new_order: bool
    new_subscription: bool

class OrganizationProfileSettings(TypedDict):
    enabled: NotRequired[bool | None]
    description: NotRequired[str | None]
    featured_projects: NotRequired[list[str] | None]
    featured_organizations: NotRequired[list[str] | None]
    links: NotRequired[list[str] | None]
    subscribe: NotRequired[OrganizationSubscribePromoteSettings | None]
    accent_color: NotRequired[str | None]

class OrganizationSocialLink(TypedDict):
    platform: OrganizationSocialPlatforms
    url: str

class OrganizationSubscribePromoteSettings(TypedDict):
    promote: NotRequired[bool]
    show_count: NotRequired[bool]
    count_free: NotRequired[bool]

class OrganizationSubscriptionSettings(TypedDict):
    allow_multiple_subscriptions: bool
    allow_customer_updates: bool
    proration_behavior: SubscriptionProrationBehavior
    benefit_revocation_grace_period: int
    prevent_trial_abuse: bool

class OrganizationUpdate(TypedDict):
    name: NotRequired[str | None]
    avatar_url: NotRequired[str | None]
    email: NotRequired[str | None]
    website: NotRequired[str | None]
    socials: NotRequired[list[OrganizationSocialLink] | None]
    details: NotRequired[OrganizationDetails | None]
    feature_settings: NotRequired[OrganizationFeatureSettings | None]
    subscription_settings: NotRequired[OrganizationSubscriptionSettings | None]
    notification_settings: NotRequired[OrganizationNotificationSettings | None]
    customer_email_settings: NotRequired[OrganizationCustomerEmailSettings | None]
    customer_portal_settings: NotRequired[OrganizationCustomerPortalSettings | None]
    default_presentment_currency: NotRequired[PresentmentCurrency | None]

class OwnerCreate(TypedDict):
    """Schema for creating an owner member during customer creation."""
    email: NotRequired[str | None]
    name: NotRequired[str | None]
    external_id: NotRequired[str | None]

class Pagination(TypedDict):
    total_count: int
    max_page: int

class PaymentAlreadyInProgress(TypedDict):
    error: Literal['PaymentAlreadyInProgress']
    detail: str

class PaymentError(TypedDict):
    error: Literal['PaymentError']
    detail: str

class PaymentMethodCard(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    processor: PaymentProcessor
    customer_id: str
    type: Literal['card']
    method_metadata: PaymentMethodCardMetadata

class PaymentMethodCardMetadata(TypedDict):
    brand: str
    last4: str
    exp_month: int
    exp_year: int
    wallet: NotRequired[str | None]

class PaymentMethodGeneric(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    processor: PaymentProcessor
    customer_id: str
    type: str

class PaymentMethodInUseByActiveSubscription(TypedDict):
    error: Literal['PaymentMethodInUseByActiveSubscription']
    detail: str

class PaymentNotReady(TypedDict):
    error: Literal['PaymentNotReady']
    detail: str

class PortalAuthenticatedUser(TypedDict):
    """Information about the authenticated portal user."""
    type: str
    name: str | None
    email: str
    customer_id: str
    member_id: NotRequired[str | None]
    role: NotRequired[str | None]

class Product(TypedDict):
    """A product."""
    id: str
    created_at: str
    modified_at: str | None
    trial_interval: TrialInterval | None
    trial_interval_count: int | None
    name: str
    description: str | None
    visibility: ProductVisibility
    recurring_interval: SubscriptionRecurringInterval | None
    recurring_interval_count: int | None
    is_recurring: bool
    is_archived: bool
    organization_id: str
    metadata: MetadataOutputType
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    benefits: list[Benefit]
    medias: list[ProductMediaFileRead]
    attached_custom_fields: list[AttachedCustomField]

class ProductBenefitsUpdate(TypedDict):
    """Schema to update the benefits granted by a product."""
    benefits: list[str]

class ProductCreateOneTime(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    name: str
    description: NotRequired[str | None]
    visibility: NotRequired[ProductVisibility]
    prices: list[ProductPriceFixedCreate | ProductPriceCustomCreate | ProductPriceFreeCreate | ProductPriceSeatBasedCreate | ProductPriceMeteredUnitCreate]
    medias: NotRequired[list[str] | None]
    attached_custom_fields: NotRequired[list[AttachedCustomFieldCreate]]
    organization_id: NotRequired[str | None]
    recurring_interval: NotRequired[None]
    recurring_interval_count: NotRequired[None]

class ProductCreateRecurring(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    name: str
    description: NotRequired[str | None]
    visibility: NotRequired[ProductVisibility]
    prices: list[ProductPriceFixedCreate | ProductPriceCustomCreate | ProductPriceFreeCreate | ProductPriceSeatBasedCreate | ProductPriceMeteredUnitCreate]
    medias: NotRequired[list[str] | None]
    attached_custom_fields: NotRequired[list[AttachedCustomFieldCreate]]
    organization_id: NotRequired[str | None]
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    recurring_interval: SubscriptionRecurringInterval
    recurring_interval_count: NotRequired[int]

class ProductMediaFileCreate(TypedDict):
    """Schema to create a file to be used as a product media file."""
    organization_id: NotRequired[str | None]
    name: str
    mime_type: str
    size: int
    checksum_sha256_base64: NotRequired[str | None]
    upload: S3FileCreateMultipart
    service: Literal['product_media']
    version: NotRequired[str | None]

class ProductMediaFileRead(TypedDict):
    """File to be used as a product media file."""
    id: str
    organization_id: str
    name: str
    path: str
    mime_type: str
    size: int
    storage_version: str | None
    checksum_etag: str | None
    checksum_sha256_base64: str | None
    checksum_sha256_hex: str | None
    last_modified_at: str | None
    version: str | None
    service: Literal['product_media']
    is_uploaded: bool
    created_at: str
    size_readable: str
    public_url: str

class ProductPriceCustom(TypedDict):
    """A pay-what-you-want price for a product."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['custom']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: ProductPriceType
    recurring_interval: SubscriptionRecurringInterval | None
    minimum_amount: int
    maximum_amount: int | None
    preset_amount: int | None

class ProductPriceCustomCreate(TypedDict):
    """Schema to create a pay-what-you-want price."""
    amount_type: Literal['custom']
    price_currency: NotRequired[PresentmentCurrency]
    minimum_amount: NotRequired[int]
    maximum_amount: NotRequired[int | None]
    preset_amount: NotRequired[int | None]

class ProductPriceFixed(TypedDict):
    """A fixed price for a product."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['fixed']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: ProductPriceType
    recurring_interval: SubscriptionRecurringInterval | None
    price_amount: int

class ProductPriceFixedCreate(TypedDict):
    """Schema to create a fixed price."""
    amount_type: Literal['fixed']
    price_currency: NotRequired[PresentmentCurrency]
    price_amount: int

class ProductPriceFree(TypedDict):
    """A free price for a product."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['free']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: ProductPriceType
    recurring_interval: SubscriptionRecurringInterval | None

class ProductPriceFreeCreate(TypedDict):
    """Schema to create a free price."""
    amount_type: Literal['free']
    price_currency: NotRequired[PresentmentCurrency]

class ProductPriceMeter(TypedDict):
    """A meter associated to a metered price."""
    id: str
    name: str

class ProductPriceMeteredUnit(TypedDict):
    """A metered, usage-based, price for a product, with a fixed unit price."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['metered_unit']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: ProductPriceType
    recurring_interval: SubscriptionRecurringInterval | None
    unit_amount: str
    cap_amount: int | None
    meter_id: str
    meter: ProductPriceMeter

class ProductPriceMeteredUnitCreate(TypedDict):
    """Schema to create a metered price with a fixed unit price."""
    amount_type: Literal['metered_unit']
    price_currency: NotRequired[PresentmentCurrency]
    meter_id: str
    unit_amount: float | str
    cap_amount: NotRequired[int | None]

class ProductPriceSeatBased(TypedDict):
    """A seat-based price for a product."""
    created_at: str
    modified_at: str | None
    id: str
    source: ProductPriceSource
    amount_type: Literal['seat_based']
    price_currency: PresentmentCurrency
    is_archived: bool
    product_id: str
    type: ProductPriceType
    recurring_interval: SubscriptionRecurringInterval | None
    seat_tiers: ProductPriceSeatTiersOutput

class ProductPriceSeatBasedCreate(TypedDict):
    """Schema to create a seat-based price with volume-based tiers."""
    amount_type: Literal['seat_based']
    price_currency: NotRequired[PresentmentCurrency]
    seat_tiers: ProductPriceSeatTiersInput

class ProductPriceSeatTier(TypedDict):
    """A pricing tier for seat-based pricing."""
    min_seats: int
    max_seats: NotRequired[int | None]
    price_per_seat: int

class ProductPriceSeatTiersInput(TypedDict):
    """List of pricing tiers for seat-based pricing.

The minimum and maximum seat limits are derived from the tiers:
- minimum_seats = first tier's min_seats
- maximum_seats = last tier's max_seats (None for unlimited)"""
    tiers: list[ProductPriceSeatTier]

class ProductPriceSeatTiersOutput(TypedDict):
    """List of pricing tiers for seat-based pricing.

The minimum and maximum seat limits are derived from the tiers:
- minimum_seats = first tier's min_seats
- maximum_seats = last tier's max_seats (None for unlimited)"""
    tiers: list[ProductPriceSeatTier]
    minimum_seats: int
    maximum_seats: int | None

class ProductUpdate(TypedDict):
    """Schema to update a product."""
    metadata: NotRequired[dict[str, Any]]
    trial_interval: NotRequired[TrialInterval | None]
    trial_interval_count: NotRequired[int | None]
    name: NotRequired[str | None]
    description: NotRequired[str | None]
    recurring_interval: NotRequired[SubscriptionRecurringInterval | None]
    recurring_interval_count: NotRequired[int | None]
    is_archived: NotRequired[bool | None]
    visibility: NotRequired[ProductVisibility | None]
    prices: NotRequired[list[ExistingProductPrice | (ProductPriceFixedCreate | ProductPriceCustomCreate | ProductPriceFreeCreate | ProductPriceSeatBasedCreate | ProductPriceMeteredUnitCreate)] | None]
    medias: NotRequired[list[str] | None]
    attached_custom_fields: NotRequired[list[AttachedCustomFieldCreate] | None]

class PropertyAggregation(TypedDict):
    func: Literal['sum', 'max', 'min', 'avg']
    property: str

class Refund(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    metadata: MetadataOutputType
    status: RefundStatus
    reason: RefundReason
    amount: int
    tax_amount: int
    currency: str
    organization_id: str
    order_id: str
    subscription_id: str | None
    customer_id: str
    revoke_benefits: bool
    dispute: RefundDispute | None

class RefundCreate(TypedDict):
    metadata: NotRequired[dict[str, Any]]
    order_id: str
    reason: RefundReason
    amount: int
    comment: NotRequired[str | None]
    revoke_benefits: NotRequired[bool]

class RefundDispute(TypedDict):
    """Dispute associated with a refund,
in case we prevented a dispute by issuing a refund."""
    created_at: str
    modified_at: str | None
    id: str
    status: DisputeStatus
    resolved: bool
    closed: bool
    amount: int
    tax_amount: int
    currency: str
    order_id: str
    payment_id: str

class RefundedAlready(TypedDict):
    error: Literal['RefundedAlready']
    detail: str

class ResourceNotFound(TypedDict):
    error: Literal['ResourceNotFound']
    detail: str

class RevokeTokenResponse(TypedDict):
    pass

class S3DownloadURL(TypedDict):
    url: str
    headers: NotRequired[dict[str, Any]]
    expires_at: str

class S3FileCreateMultipart(TypedDict):
    parts: list[S3FileCreatePart]

class S3FileCreatePart(TypedDict):
    number: int
    chunk_start: int
    chunk_end: int
    checksum_sha256_base64: NotRequired[str | None]

class S3FileUploadCompletedPart(TypedDict):
    number: int
    checksum_etag: str
    checksum_sha256_base64: str | None

class S3FileUploadMultipart(TypedDict):
    id: str
    path: str
    parts: list[S3FileUploadPart]

class S3FileUploadPart(TypedDict):
    number: int
    chunk_start: int
    chunk_end: int
    checksum_sha256_base64: NotRequired[str | None]
    url: str
    expires_at: str
    headers: NotRequired[dict[str, Any]]

class SeatAssign(TypedDict):
    subscription_id: NotRequired[str | None]
    checkout_id: NotRequired[str | None]
    order_id: NotRequired[str | None]
    email: NotRequired[str | None]
    external_customer_id: NotRequired[str | None]
    customer_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    member_id: NotRequired[str | None]
    metadata: NotRequired[dict[str, Any] | None]
    immediate_claim: NotRequired[bool]

class SeatClaim(TypedDict):
    invitation_token: str

class SeatClaimInfo(TypedDict):
    """Read-only information about a seat claim invitation.
Safe for email scanners - no side effects when fetched."""
    product_name: str
    product_id: str
    organization_name: str
    organization_slug: str
    customer_email: str
    can_claim: bool

class SeatsList(TypedDict):
    seats: list[CustomerSeat]
    available_seats: int
    total_seats: int

class Subscription(TypedDict):
    created_at: str
    modified_at: str | None
    id: str
    amount: int
    currency: str
    recurring_interval: SubscriptionRecurringInterval
    recurring_interval_count: int
    status: SubscriptionStatus
    current_period_start: str
    current_period_end: str | None
    trial_start: str | None
    trial_end: str | None
    cancel_at_period_end: bool
    canceled_at: str | None
    started_at: str | None
    ends_at: str | None
    ended_at: str | None
    customer_id: str
    product_id: str
    discount_id: str | None
    checkout_id: str | None
    seats: NotRequired[int | None]
    customer_cancellation_reason: CustomerCancellationReason | None
    customer_cancellation_comment: str | None
    metadata: MetadataOutputType
    custom_field_data: NotRequired[dict[str, Any]]
    customer: SubscriptionCustomer
    product: Product
    discount: DiscountFixedOnceForeverDurationBase | DiscountFixedRepeatDurationBase | DiscountPercentageOnceForeverDurationBase | DiscountPercentageRepeatDurationBase | None
    prices: list[LegacyRecurringProductPrice | ProductPrice]
    meters: list[SubscriptionMeter]

class SubscriptionBillingPeriodUpdatedEvent(TypedDict):
    """An event created by Polar when a subscription billing period is updated."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.billing_period_updated']
    metadata: SubscriptionBillingPeriodUpdatedMetadata

class SubscriptionBillingPeriodUpdatedMetadata(TypedDict):
    subscription_id: str
    old_period_end: str
    new_period_end: str

class SubscriptionCancel(TypedDict):
    customer_cancellation_reason: NotRequired[CustomerCancellationReason | None]
    customer_cancellation_comment: NotRequired[str | None]
    cancel_at_period_end: bool

class SubscriptionCanceledEvent(TypedDict):
    """An event created by Polar when a subscription is canceled."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.canceled']
    metadata: SubscriptionCanceledMetadata

class SubscriptionCanceledMetadata(TypedDict):
    subscription_id: str
    product_id: NotRequired[str]
    amount: int
    currency: str
    recurring_interval: str
    recurring_interval_count: int
    customer_cancellation_reason: NotRequired[str]
    customer_cancellation_comment: NotRequired[str]
    canceled_at: str
    ends_at: NotRequired[str]
    cancel_at_period_end: NotRequired[bool]

class SubscriptionCreateCustomer(TypedDict):
    """Create a subscription for an existing customer."""
    metadata: NotRequired[dict[str, Any]]
    product_id: str
    customer_id: str

class SubscriptionCreateExternalCustomer(TypedDict):
    """Create a subscription for an existing customer identified by an external ID."""
    metadata: NotRequired[dict[str, Any]]
    product_id: str
    external_customer_id: str

class SubscriptionCreatedEvent(TypedDict):
    """An event created by Polar when a subscription is created."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.created']
    metadata: SubscriptionCreatedMetadata

class SubscriptionCreatedMetadata(TypedDict):
    subscription_id: str
    product_id: str
    amount: int
    currency: str
    recurring_interval: str
    recurring_interval_count: int
    started_at: str

class SubscriptionCustomer(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    metadata: MetadataOutputType
    external_id: str | None
    email: str
    email_verified: bool
    type: NotRequired[CustomerType | None]
    name: str | None
    billing_address: Address | None
    tax_id: list[Any] | None
    locale: NotRequired[str | None]
    organization_id: str
    deleted_at: str | None
    avatar_url: str

class SubscriptionCycledEvent(TypedDict):
    """An event created by Polar when a subscription is cycled."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.cycled']
    metadata: SubscriptionCycledMetadata

class SubscriptionCycledMetadata(TypedDict):
    subscription_id: str
    product_id: NotRequired[str]
    amount: NotRequired[int]
    currency: NotRequired[str]
    recurring_interval: NotRequired[str]
    recurring_interval_count: NotRequired[int]

class SubscriptionLocked(TypedDict):
    error: Literal['SubscriptionLocked']
    detail: str

class SubscriptionMeter(TypedDict):
    """Current consumption and spending for a subscription meter."""
    created_at: str
    modified_at: str | None
    id: str
    consumed_units: float
    credited_units: int
    amount: int
    meter_id: str
    meter: Meter

class SubscriptionProductUpdatedEvent(TypedDict):
    """An event created by Polar when a subscription changes the product."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.product_updated']
    metadata: SubscriptionProductUpdatedMetadata

class SubscriptionProductUpdatedMetadata(TypedDict):
    subscription_id: str
    old_product_id: str
    new_product_id: str

class SubscriptionRevoke(TypedDict):
    customer_cancellation_reason: NotRequired[CustomerCancellationReason | None]
    customer_cancellation_comment: NotRequired[str | None]
    revoke: Literal[True]

class SubscriptionRevokedEvent(TypedDict):
    """An event created by Polar when a subscription is revoked from a customer."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.revoked']
    metadata: SubscriptionRevokedMetadata

class SubscriptionRevokedMetadata(TypedDict):
    subscription_id: str
    product_id: NotRequired[str]
    amount: NotRequired[int]
    currency: NotRequired[str]
    recurring_interval: NotRequired[str]
    recurring_interval_count: NotRequired[int]

class SubscriptionSeatsUpdatedEvent(TypedDict):
    """An event created by Polar when a the seats on a subscription is changed."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.seats_updated']
    metadata: SubscriptionSeatsUpdatedMetadata

class SubscriptionSeatsUpdatedMetadata(TypedDict):
    subscription_id: str
    old_seats: int
    new_seats: int
    proration_behavior: str

class SubscriptionUncanceledEvent(TypedDict):
    """An event created by Polar when a subscription cancellation is reversed."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    source: Literal['system']
    name: Literal['subscription.uncanceled']
    metadata: SubscriptionUncanceledMetadata

class SubscriptionUncanceledMetadata(TypedDict):
    subscription_id: str
    product_id: str
    amount: int
    currency: str
    recurring_interval: str
    recurring_interval_count: int

class SubscriptionUpdateBillingPeriod(TypedDict):
    current_billing_period_end: str

class SubscriptionUpdateDiscount(TypedDict):
    discount_id: str | None

class SubscriptionUpdateProduct(TypedDict):
    product_id: str
    proration_behavior: NotRequired[SubscriptionProrationBehavior | None]

class SubscriptionUpdateSeats(TypedDict):
    seats: int
    proration_behavior: NotRequired[SubscriptionProrationBehavior | None]

class SubscriptionUpdateTrial(TypedDict):
    trial_end: str | Literal['now']

class SubscriptionUser(TypedDict):
    id: str
    email: str
    public_name: str
    avatar_url: NotRequired[str | None]
    github_username: NotRequired[str | None]

class TokenResponse(TypedDict):
    access_token: str
    token_type: Literal['Bearer']
    expires_in: int
    refresh_token: str | None
    scope: str
    id_token: str

class TrialAlreadyRedeemed(TypedDict):
    error: Literal['TrialAlreadyRedeemed']
    detail: str

class Unauthorized(TypedDict):
    error: Literal['Unauthorized']
    detail: str

class UniqueAggregation(TypedDict):
    func: NotRequired[Literal['unique']]
    property: str

class UserEvent(TypedDict):
    """An event you created through the ingestion API."""
    id: str
    timestamp: str
    organization_id: str
    customer_id: str | None
    customer: Customer | None
    external_customer_id: str | None
    member_id: NotRequired[str | None]
    external_member_id: NotRequired[str | None]
    child_count: NotRequired[int]
    parent_id: NotRequired[str | None]
    label: str
    name: str
    source: Literal['user']
    metadata: EventMetadataOutput

class UserInfoOrganization(TypedDict):
    sub: str
    name: NotRequired[str | None]

class UserInfoUser(TypedDict):
    sub: str
    name: NotRequired[str | None]
    email: NotRequired[str | None]
    email_verified: NotRequired[bool | None]

class ValidatedLicenseKey(TypedDict):
    id: str
    created_at: str
    modified_at: str | None
    organization_id: str
    customer_id: str
    customer: LicenseKeyCustomer
    benefit_id: str
    key: str
    display_key: str
    status: LicenseKeyStatus
    limit_activations: int | None
    usage: int
    limit_usage: int | None
    validations: int
    last_validated_at: str | None
    expires_at: str | None
    activation: NotRequired[LicenseKeyActivationBase | None]

class ValidationError(TypedDict):
    loc: list[str | int]
    msg: str
    type: str
    input: NotRequired[Any]
    ctx: NotRequired[dict[str, Any]]

class WebhookBenefitCreatedPayload(TypedDict):
    """Sent when a new benefit is created.

**Discord & Slack support:** Basic"""
    type: Literal['benefit.created']
    timestamp: str
    data: Benefit

class WebhookBenefitGrantCreatedPayload(TypedDict):
    """Sent when a new benefit grant is created.

**Discord & Slack support:** Basic"""
    type: Literal['benefit_grant.created']
    timestamp: str
    data: BenefitGrantWebhook

class WebhookBenefitGrantCycledPayload(TypedDict):
    """Sent when a benefit grant is cycled,
meaning the related subscription has been renewed for another period.

**Discord & Slack support:** Basic"""
    type: Literal['benefit_grant.cycled']
    timestamp: str
    data: BenefitGrantWebhook

class WebhookBenefitGrantRevokedPayload(TypedDict):
    """Sent when a benefit grant is revoked.

**Discord & Slack support:** Basic"""
    type: Literal['benefit_grant.revoked']
    timestamp: str
    data: BenefitGrantWebhook

class WebhookBenefitGrantUpdatedPayload(TypedDict):
    """Sent when a benefit grant is updated.

**Discord & Slack support:** Basic"""
    type: Literal['benefit_grant.updated']
    timestamp: str
    data: BenefitGrantWebhook

class WebhookBenefitUpdatedPayload(TypedDict):
    """Sent when a benefit is updated.

**Discord & Slack support:** Basic"""
    type: Literal['benefit.updated']
    timestamp: str
    data: Benefit

class WebhookCheckoutCreatedPayload(TypedDict):
    """Sent when a new checkout is created.

**Discord & Slack support:** Basic"""
    type: Literal['checkout.created']
    timestamp: str
    data: Checkout

class WebhookCheckoutExpiredPayload(TypedDict):
    """Sent when a checkout expires.

This event fires when a checkout reaches its expiration time without being completed.
Developers can use this to send reminder emails or track checkout abandonment.

**Discord & Slack support:** Basic"""
    type: Literal['checkout.expired']
    timestamp: str
    data: Checkout

class WebhookCheckoutUpdatedPayload(TypedDict):
    """Sent when a checkout is updated.

**Discord & Slack support:** Basic"""
    type: Literal['checkout.updated']
    timestamp: str
    data: Checkout

class WebhookCustomerCreatedPayload(TypedDict):
    """Sent when a new customer is created.

A customer can be created:

* After a successful checkout.
* Programmatically via the API.

**Discord & Slack support:** Basic"""
    type: Literal['customer.created']
    timestamp: str
    data: Customer

class WebhookCustomerDeletedPayload(TypedDict):
    """Sent when a customer is deleted.

**Discord & Slack support:** Basic"""
    type: Literal['customer.deleted']
    timestamp: str
    data: Customer

class WebhookCustomerSeatAssignedPayload(TypedDict):
    """Sent when a new customer seat is assigned.

This event is triggered when a seat is assigned to a customer by the organization.
The customer will receive an invitation email to claim the seat."""
    type: Literal['customer_seat.assigned']
    timestamp: str
    data: CustomerSeat

class WebhookCustomerSeatClaimedPayload(TypedDict):
    """Sent when a customer seat is claimed.

This event is triggered when a customer accepts the seat invitation and claims their access."""
    type: Literal['customer_seat.claimed']
    timestamp: str
    data: CustomerSeat

class WebhookCustomerSeatRevokedPayload(TypedDict):
    """Sent when a customer seat is revoked.

This event is triggered when access to a seat is revoked, either manually by the organization or automatically when a subscription is canceled."""
    type: Literal['customer_seat.revoked']
    timestamp: str
    data: CustomerSeat

class WebhookCustomerStateChangedPayload(TypedDict):
    """Sent when a customer state has changed.

It's triggered when:

* Customer is created, updated or deleted.
* A subscription is created or updated.
* A benefit is granted or revoked.

**Discord & Slack support:** Basic"""
    type: Literal['customer.state_changed']
    timestamp: str
    data: CustomerState

class WebhookCustomerUpdatedPayload(TypedDict):
    """Sent when a customer is updated.

This event is fired when the customer details are updated.

If you want to be notified when a customer subscription or benefit state changes, you should listen to the `customer_state_changed` event.

**Discord & Slack support:** Basic"""
    type: Literal['customer.updated']
    timestamp: str
    data: Customer

class WebhookDelivery(TypedDict):
    """A webhook delivery for a webhook event."""
    created_at: str
    modified_at: str | None
    id: str
    succeeded: bool
    http_code: int | None
    response: str | None
    webhook_event: WebhookEvent

class WebhookEndpoint(TypedDict):
    """A webhook endpoint."""
    created_at: str
    modified_at: str | None
    id: str
    url: str
    format: WebhookFormat
    secret: str
    organization_id: str
    events: list[WebhookEventType]
    enabled: bool

class WebhookEndpointCreate(TypedDict):
    """Schema to create a webhook endpoint."""
    url: str
    secret: NotRequired[str | None]
    format: WebhookFormat
    events: list[WebhookEventType]
    organization_id: NotRequired[str | None]

class WebhookEndpointUpdate(TypedDict):
    """Schema to update a webhook endpoint."""
    url: NotRequired[str | None]
    secret: NotRequired[str | None]
    format: NotRequired[WebhookFormat | None]
    events: NotRequired[list[WebhookEventType] | None]
    enabled: NotRequired[bool | None]

class WebhookEvent(TypedDict):
    """A webhook event.

An event represent something that happened in the system
that should be sent to the webhook endpoint.

It can be delivered multiple times until it's marked as succeeded,
each one creating a new delivery."""
    created_at: str
    modified_at: str | None
    id: str
    last_http_code: NotRequired[int | None]
    succeeded: NotRequired[bool | None]
    skipped: bool
    payload: str | None
    type: WebhookEventType
    is_archived: bool

class WebhookMemberCreatedPayload(TypedDict):
    """Sent when a new member is created.

A member represents an individual within a customer (team).
This event is triggered when a member is added to a customer,
either programmatically via the API or when an owner is automatically
created for a new customer.

**Discord & Slack support:** Basic"""
    type: Literal['member.created']
    timestamp: str
    data: Member

class WebhookMemberDeletedPayload(TypedDict):
    """Sent when a member is deleted.

This event is triggered when a member is removed from a customer.
Any active seats assigned to the member will be automatically revoked.

**Discord & Slack support:** Basic"""
    type: Literal['member.deleted']
    timestamp: str
    data: Member

class WebhookMemberUpdatedPayload(TypedDict):
    """Sent when a member is updated.

This event is triggered when member details are updated,
such as their name or role within the customer.

**Discord & Slack support:** Basic"""
    type: Literal['member.updated']
    timestamp: str
    data: Member

class WebhookOrderCreatedPayload(TypedDict):
    """Sent when a new order is created.

A new order is created when:

* A customer purchases a one-time product. In this case, `billing_reason` is set to `purchase`.
* A customer starts a subscription. In this case, `billing_reason` is set to `subscription_create`.
* A subscription is renewed. In this case, `billing_reason` is set to `subscription_cycle`.
* A subscription is upgraded or downgraded with an immediate proration invoice. In this case, `billing_reason` is set to `subscription_update`.

> [!WARNING]
> The order might not be paid yet, so the `status` field might be `pending`.

**Discord & Slack support:** Full"""
    type: Literal['order.created']
    timestamp: str
    data: Order

class WebhookOrderPaidPayload(TypedDict):
    """Sent when an order is paid.

When you receive this event, the order is fully processed and payment has been received.

**Discord & Slack support:** Full"""
    type: Literal['order.paid']
    timestamp: str
    data: Order

class WebhookOrderRefundedPayload(TypedDict):
    """Sent when an order is fully or partially refunded.

**Discord & Slack support:** Full"""
    type: Literal['order.refunded']
    timestamp: str
    data: Order

class WebhookOrderUpdatedPayload(TypedDict):
    """Sent when an order is updated.

An order is updated when:

* Its status changes, e.g. from `pending` to `paid`.
* It's refunded, partially or fully.

**Discord & Slack support:** Full"""
    type: Literal['order.updated']
    timestamp: str
    data: Order

class WebhookOrganizationUpdatedPayload(TypedDict):
    """Sent when a organization is updated.

**Discord & Slack support:** Basic"""
    type: Literal['organization.updated']
    timestamp: str
    data: Organization

class WebhookProductCreatedPayload(TypedDict):
    """Sent when a new product is created.

**Discord & Slack support:** Basic"""
    type: Literal['product.created']
    timestamp: str
    data: Product

class WebhookProductUpdatedPayload(TypedDict):
    """Sent when a product is updated.

**Discord & Slack support:** Basic"""
    type: Literal['product.updated']
    timestamp: str
    data: Product

class WebhookRefundCreatedPayload(TypedDict):
    """Sent when a refund is created regardless of status.

**Discord & Slack support:** Full"""
    type: Literal['refund.created']
    timestamp: str
    data: Refund

class WebhookRefundUpdatedPayload(TypedDict):
    """Sent when a refund is updated.

**Discord & Slack support:** Full"""
    type: Literal['refund.updated']
    timestamp: str
    data: Refund

class WebhookSubscriptionActivePayload(TypedDict):
    """Sent when a subscription becomes active,
whether because it's a new paid subscription or because payment was recovered.

**Discord & Slack support:** Full"""
    type: Literal['subscription.active']
    timestamp: str
    data: Subscription

class WebhookSubscriptionCanceledPayload(TypedDict):
    """Sent when a subscription is canceled.
Customers might still have access until the end of the current period.

**Discord & Slack support:** Full"""
    type: Literal['subscription.canceled']
    timestamp: str
    data: Subscription

class WebhookSubscriptionCreatedPayload(TypedDict):
    """Sent when a new subscription is created.

When this event occurs, the subscription `status` might not be `active` yet, as we can still have to wait for the first payment to be processed.

**Discord & Slack support:** Full"""
    type: Literal['subscription.created']
    timestamp: str
    data: Subscription

class WebhookSubscriptionPastDuePayload(TypedDict):
    """Sent when a subscription payment fails and the subscription enters `past_due` status.

This is a recoverable state - the customer can update their payment method to restore the subscription.
Benefits may be revoked depending on the organization's grace period settings.

If payment retries are exhausted, a `subscription.revoked` event will be sent.

**Discord & Slack support:** Full"""
    type: Literal['subscription.past_due']
    timestamp: str
    data: Subscription

class WebhookSubscriptionRevokedPayload(TypedDict):
    """Sent when a subscription is revoked and the user loses access immediately.
Happens when the subscription is canceled or payment retries are exhausted (status becomes `unpaid`).

For payment failures that can still be recovered, see `subscription.past_due`.

**Discord & Slack support:** Full"""
    type: Literal['subscription.revoked']
    timestamp: str
    data: Subscription

class WebhookSubscriptionUncanceledPayload(TypedDict):
    """Sent when a customer revokes a pending cancellation.

When a customer cancels with "at period end", they retain access until the
subscription would renew. During this time, they can change their mind and
undo the cancellation. This event is triggered when they do so.

**Discord & Slack support:** Full"""
    type: Literal['subscription.uncanceled']
    timestamp: str
    data: Subscription

class WebhookSubscriptionUpdatedPayload(TypedDict):
    """Sent when a subscription is updated. This event fires for all changes to the subscription, including renewals.

If you want more specific events, you can listen to `subscription.active`, `subscription.canceled`, `subscription.past_due`, and `subscription.revoked`.

To listen specifically for renewals, you can listen to `order.created` events and check the `billing_reason` field.

**Discord & Slack support:** On cancellation, past due, and revocation. Renewals are skipped."""
    type: Literal['subscription.updated']
    timestamp: str
    data: Subscription

class AuthorizationCodeTokenRequest(TypedDict):
    grant_type: Literal['authorization_code']
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str

class RefreshTokenRequest(TypedDict):
    grant_type: Literal['refresh_token']
    client_id: str
    client_secret: str
    refresh_token: str

class WebTokenRequest(TypedDict):
    grant_type: Literal['web']
    client_id: str
    client_secret: str
    session_token: str
    sub_type: NotRequired[Literal['user', 'organization']]
    sub: NotRequired[str | None]
    scope: NotRequired[str | None]

class RevokeTokenRequest(TypedDict):
    token: str
    token_type_hint: NotRequired[Literal['access_token', 'refresh_token'] | None]
    client_id: str
    client_secret: str

class IntrospectTokenRequest(TypedDict):
    token: str
    token_type_hint: NotRequired[Literal['access_token', 'refresh_token'] | None]
    client_id: str
    client_secret: str
AggregationFunction = Literal['count', 'sum', 'max', 'min', 'avg', 'unique']
AvailableScope = Literal['openid', 'profile', 'email', 'user:read', 'user:write', 'organizations:read', 'organizations:write', 'custom_fields:read', 'custom_fields:write', 'discounts:read', 'discounts:write', 'checkout_links:read', 'checkout_links:write', 'checkouts:read', 'checkouts:write', 'transactions:read', 'transactions:write', 'payouts:read', 'payouts:write', 'products:read', 'products:write', 'benefits:read', 'benefits:write', 'events:read', 'events:write', 'meters:read', 'meters:write', 'files:read', 'files:write', 'subscriptions:read', 'subscriptions:write', 'customers:read', 'customers:write', 'members:read', 'members:write', 'wallets:read', 'wallets:write', 'disputes:read', 'customer_meters:read', 'customer_sessions:write', 'member_sessions:write', 'customer_seats:read', 'customer_seats:write', 'orders:read', 'orders:write', 'refunds:read', 'refunds:write', 'payments:read', 'metrics:read', 'webhooks:read', 'webhooks:write', 'license_keys:read', 'license_keys:write', 'customer_portal:read', 'customer_portal:write', 'notifications:read', 'notifications:write', 'notification_recipients:read', 'notification_recipients:write', 'organization_access_tokens:read', 'organization_access_tokens:write']
Benefit = BenefitCustom | BenefitDiscord | BenefitGitHubRepository | BenefitDownloadables | BenefitLicenseKeys | BenefitMeterCredit
BenefitCreate = BenefitCustomCreate | BenefitDiscordCreate | BenefitGitHubRepositoryCreate | BenefitDownloadablesCreate | BenefitLicenseKeysCreate | BenefitMeterCreditCreate
BenefitGrantSortProperty = Literal['created_at', '-created_at', 'granted_at', '-granted_at', 'revoked_at', '-revoked_at']
BenefitGrantWebhook = BenefitGrantDiscordWebhook | BenefitGrantCustomWebhook | BenefitGrantGitHubRepositoryWebhook | BenefitGrantDownloadablesWebhook | BenefitGrantLicenseKeysWebhook | BenefitGrantMeterCreditWebhook
BenefitSortProperty = Literal['created_at', '-created_at', 'description', '-description', 'type', '-type', 'user_order', '-user_order']
BenefitType = Literal['custom', 'discord', 'github_repository', 'downloadables', 'license_keys', 'meter_credit']
BillingAddressFieldMode = Literal['required', 'optional', 'disabled']
CheckoutCreate = CheckoutProductsCreate
CheckoutForbiddenError = AlreadyActiveSubscriptionError | NotOpenCheckout | PaymentNotReady | TrialAlreadyRedeemed
CheckoutLinkCreate = CheckoutLinkCreateProductPrice | CheckoutLinkCreateProduct | CheckoutLinkCreateProducts
CheckoutLinkSortProperty = Literal['created_at', '-created_at', 'label', '-label', 'success_url', '-success_url', 'allow_discount_codes', '-allow_discount_codes']
CheckoutSortProperty = Literal['created_at', '-created_at', 'expires_at', '-expires_at', 'status', '-status']
CheckoutStatus = Literal['open', 'expired', 'confirmed', 'succeeded', 'failed']
CountryAlpha2 = Literal['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW']
CountryAlpha2Input = Literal['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW']
CustomField = CustomFieldText | CustomFieldNumber | CustomFieldDate | CustomFieldCheckbox | CustomFieldSelect
CustomFieldCreate = CustomFieldCreateText | CustomFieldCreateNumber | CustomFieldCreateDate | CustomFieldCreateCheckbox | CustomFieldCreateSelect
CustomFieldSortProperty = Literal['created_at', '-created_at', 'slug', '-slug', 'name', '-name', 'type', '-type']
CustomFieldType = Literal['text', 'number', 'date', 'checkbox', 'select']
CustomFieldUpdate = CustomFieldUpdateText | CustomFieldUpdateNumber | CustomFieldUpdateDate | CustomFieldUpdateCheckbox | CustomFieldUpdateSelect
CustomerBenefitGrant = CustomerBenefitGrantDiscord | CustomerBenefitGrantGitHubRepository | CustomerBenefitGrantDownloadables | CustomerBenefitGrantLicenseKeys | CustomerBenefitGrantCustom | CustomerBenefitGrantMeterCredit
CustomerBenefitGrantSortProperty = Literal['granted_at', '-granted_at', 'type', '-type', 'organization', '-organization', 'product_benefit', '-product_benefit']
CustomerBenefitGrantUpdate = CustomerBenefitGrantDiscordUpdate | CustomerBenefitGrantGitHubRepositoryUpdate | CustomerBenefitGrantDownloadablesUpdate | CustomerBenefitGrantLicenseKeysUpdate | CustomerBenefitGrantCustomUpdate | CustomerBenefitGrantMeterCreditUpdate
CustomerCancellationReason = Literal['customer_service', 'low_quality', 'missing_features', 'switched_service', 'too_complex', 'too_expensive', 'unused', 'other']
CustomerCustomerMeterSortProperty = Literal['created_at', '-created_at', 'modified_at', '-modified_at', 'meter_id', '-meter_id', 'meter_name', '-meter_name', 'consumed_units', '-consumed_units', 'credited_units', '-credited_units', 'balance', '-balance']
CustomerMeterSortProperty = Literal['created_at', '-created_at', 'modified_at', '-modified_at', 'customer_id', '-customer_id', 'customer_name', '-customer_name', 'meter_id', '-meter_id', 'meter_name', '-meter_name', 'consumed_units', '-consumed_units', 'credited_units', '-credited_units', 'balance', '-balance']
CustomerOrderSortProperty = Literal['created_at', '-created_at', 'amount', '-amount', 'net_amount', '-net_amount', 'product', '-product', 'subscription', '-subscription']
CustomerPaymentMethod = PaymentMethodCard | PaymentMethodGeneric
CustomerPaymentMethodCreateResponse = CustomerPaymentMethodCreateSucceededResponse | CustomerPaymentMethodCreateRequiresActionResponse
CustomerSortProperty = Literal['created_at', '-created_at', 'email', '-email', 'name', '-name']
CustomerSubscriptionSortProperty = Literal['started_at', '-started_at', 'amount', '-amount', 'status', '-status', 'organization', '-organization', 'product', '-product']
CustomerSubscriptionUpdate = CustomerSubscriptionUpdateProduct | CustomerSubscriptionUpdateSeats | CustomerSubscriptionCancel
CustomerType = Literal['individual', 'team']
CustomerWalletSortProperty = Literal['created_at', '-created_at', 'balance', '-balance']
Discount = DiscountFixedOnceForeverDuration | DiscountFixedRepeatDuration | DiscountPercentageOnceForeverDuration | DiscountPercentageRepeatDuration
DiscountCreate = DiscountFixedOnceForeverDurationCreate | DiscountFixedRepeatDurationCreate | DiscountPercentageOnceForeverDurationCreate | DiscountPercentageRepeatDurationCreate
DiscountDuration = Literal['once', 'forever', 'repeating']
DiscountSortProperty = Literal['created_at', '-created_at', 'name', '-name', 'code', '-code', 'redemptions_count', '-redemptions_count']
DiscountType = Literal['fixed', 'percentage']
DisputeSortProperty = Literal['created_at', '-created_at', 'amount', '-amount']
DisputeStatus = Literal['prevented', 'early_warning', 'needs_response', 'under_review', 'lost', 'won']
Event = SystemEvent | UserEvent
EventNamesSortProperty = Literal['name', '-name', 'occurrences', '-occurrences', 'first_seen', '-first_seen', 'last_seen', '-last_seen']
EventSortProperty = Literal['timestamp', '-timestamp']
EventSource = Literal['system', 'user']
EventTypesSortProperty = Literal['name', '-name', 'label', '-label', 'occurrences', '-occurrences', 'first_seen', '-first_seen', 'last_seen', '-last_seen']
FileCreate = DownloadableFileCreate | ProductMediaFileCreate | OrganizationAvatarFileCreate
FileServiceTypes = Literal['downloadable', 'product_media', 'organization_avatar']
FilterConjunction = Literal['and', 'or']
FilterOperator = Literal['eq', 'ne', 'gt', 'gte', 'lt', 'lte', 'like', 'not_like']
LegacyOrganizationStatus = Literal['created', 'onboarding_started', 'under_review', 'denied', 'active']
LegacyRecurringProductPrice = LegacyRecurringProductPriceFixed | LegacyRecurringProductPriceCustom | LegacyRecurringProductPriceFree
LicenseKeyStatus = Literal['granted', 'revoked', 'disabled']
MemberRole = Literal['owner', 'billing_manager', 'member']
MemberSortProperty = Literal['created_at', '-created_at']
MeterSortProperty = Literal['created_at', '-created_at', 'name', '-name']
MetricType = Literal['scalar', 'currency', 'currency_sub_cent', 'percentage']
OrderBillingReason = Literal['purchase', 'subscription_create', 'subscription_cycle', 'subscription_update']
OrderBillingReasonInternal = Literal['purchase', 'subscription_create', 'subscription_cycle', 'subscription_cycle_after_trial', 'subscription_update']
OrderSortProperty = Literal['created_at', '-created_at', 'status', '-status', 'invoice_number', '-invoice_number', 'amount', '-amount', 'net_amount', '-net_amount', 'customer', '-customer', 'product', '-product', 'discount', '-discount', 'subscription', '-subscription']
OrderStatus = Literal['pending', 'paid', 'refunded', 'partially_refunded']
OrganizationAccessTokenSortProperty = Literal['created_at', '-created_at', 'comment', '-comment', 'last_used_at', '-last_used_at', 'organization_id', '-organization_id']
OrganizationSocialPlatforms = Literal['x', 'github', 'facebook', 'instagram', 'youtube', 'tiktok', 'linkedin', 'other']
OrganizationSortProperty = Literal['created_at', '-created_at', 'slug', '-slug', 'name', '-name', 'next_review_threshold', '-next_review_threshold', 'days_in_status', '-days_in_status']
OrganizationStatus = Literal['created', 'onboarding_started', 'initial_review', 'ongoing_review', 'denied', 'active']
Payment = CardPayment | GenericPayment
PaymentProcessor = Literal['stripe']
PaymentSortProperty = Literal['created_at', '-created_at', 'status', '-status', 'amount', '-amount', 'method', '-method']
PaymentStatus = Literal['pending', 'succeeded', 'failed']
PresentmentCurrency = Literal['usd']
ProductBillingType = Literal['one_time', 'recurring']
ProductCreate = ProductCreateRecurring | ProductCreateOneTime
ProductPrice = ProductPriceFixed | ProductPriceCustom | ProductPriceFree | ProductPriceSeatBased | ProductPriceMeteredUnit
ProductPriceSource = Literal['catalog', 'ad_hoc']
ProductPriceType = Literal['one_time', 'recurring']
ProductSortProperty = Literal['created_at', '-created_at', 'name', '-name', 'price_amount_type', '-price_amount_type', 'price_amount', '-price_amount']
ProductVisibility = Literal['draft', 'private', 'public']
RefundReason = Literal['duplicate', 'fraudulent', 'customer_request', 'service_disruption', 'satisfaction_guarantee', 'dispute_prevention', 'other']
RefundSortProperty = Literal['created_at', '-created_at', 'amount', '-amount']
RefundStatus = Literal['pending', 'succeeded', 'failed', 'canceled']
Scope = Literal['openid', 'profile', 'email', 'user:read', 'user:write', 'web:read', 'web:write', 'organizations:read', 'organizations:write', 'custom_fields:read', 'custom_fields:write', 'discounts:read', 'discounts:write', 'checkout_links:read', 'checkout_links:write', 'checkouts:read', 'checkouts:write', 'transactions:read', 'transactions:write', 'payouts:read', 'payouts:write', 'products:read', 'products:write', 'benefits:read', 'benefits:write', 'events:read', 'events:write', 'meters:read', 'meters:write', 'files:read', 'files:write', 'subscriptions:read', 'subscriptions:write', 'customers:read', 'customers:write', 'members:read', 'members:write', 'wallets:read', 'wallets:write', 'disputes:read', 'customer_meters:read', 'customer_sessions:write', 'member_sessions:write', 'customer_seats:read', 'customer_seats:write', 'orders:read', 'orders:write', 'refunds:read', 'refunds:write', 'payments:read', 'metrics:read', 'webhooks:read', 'webhooks:write', 'license_keys:read', 'license_keys:write', 'customer_portal:read', 'customer_portal:write', 'notifications:read', 'notifications:write', 'notification_recipients:read', 'notification_recipients:write', 'organization_access_tokens:read', 'organization_access_tokens:write']
SeatStatus = Literal['pending', 'claimed', 'revoked']
SubType = Literal['user', 'organization']
SubscriptionProrationBehavior = Literal['invoice', 'prorate']
SubscriptionRecurringInterval = Literal['day', 'week', 'month', 'year']
SubscriptionSortProperty = Literal['customer', '-customer', 'status', '-status', 'started_at', '-started_at', 'current_period_end', '-current_period_end', 'ended_at', '-ended_at', 'ends_at', '-ends_at', 'amount', '-amount', 'product', '-product', 'discount', '-discount']
SubscriptionStatus = Literal['incomplete', 'incomplete_expired', 'trialing', 'active', 'past_due', 'canceled', 'unpaid']
SubscriptionUpdate = SubscriptionUpdateProduct | SubscriptionUpdateDiscount | SubscriptionUpdateTrial | SubscriptionUpdateSeats | SubscriptionUpdateBillingPeriod | SubscriptionCancel | SubscriptionRevoke
SystemEvent = MeterCreditEvent | MeterResetEvent | BenefitGrantedEvent | BenefitCycledEvent | BenefitUpdatedEvent | BenefitRevokedEvent | SubscriptionCreatedEvent | SubscriptionCycledEvent | SubscriptionCanceledEvent | SubscriptionRevokedEvent | SubscriptionUncanceledEvent | SubscriptionProductUpdatedEvent | SubscriptionSeatsUpdatedEvent | SubscriptionBillingPeriodUpdatedEvent | OrderPaidEvent | OrderRefundedEvent | CheckoutCreatedEvent | CustomerCreatedEvent | CustomerUpdatedEvent | CustomerDeletedEvent | BalanceOrderEvent | BalanceCreditOrderEvent | BalanceRefundEvent | BalanceRefundReversalEvent | BalanceDisputeEvent | BalanceDisputeReversalEvent
TaxIDFormat = Literal['ad_nrt', 'ae_trn', 'ar_cuit', 'au_abn', 'au_arn', 'bg_uic', 'bh_vat', 'bo_tin', 'br_cnpj', 'br_cpf', 'ca_bn', 'ca_gst_hst', 'ca_pst_bc', 'ca_pst_mb', 'ca_pst_sk', 'ca_qst', 'ch_uid', 'ch_vat', 'cl_tin', 'cn_tin', 'co_nit', 'cr_tin', 'de_stn', 'do_rcn', 'ec_ruc', 'eg_tin', 'es_cif', 'eu_oss_vat', 'eu_vat', 'gb_vat', 'ge_vat', 'hk_br', 'hr_oib', 'hu_tin', 'id_npwp', 'il_vat', 'in_gst', 'is_vat', 'jp_cn', 'jp_rn', 'jp_trn', 'ke_pin', 'kr_brn', 'kz_bin', 'li_uid', 'mx_rfc', 'my_frp', 'my_itn', 'my_sst', 'ng_tin', 'no_vat', 'no_voec', 'nz_gst', 'om_vat', 'pe_ruc', 'ph_tin', 'ro_tin', 'rs_pib', 'ru_inn', 'ru_kpp', 'sa_vat', 'sg_gst', 'sg_uen', 'si_tin', 'sv_nit', 'th_vat', 'tr_tin', 'tw_vat', 'ua_vat', 'us_ein', 'uy_ruc', 've_rif', 'vn_tin', 'za_vat']
TimeInterval = Literal['year', 'month', 'week', 'day', 'hour']
TrialInterval = Literal['day', 'week', 'month', 'year']
WebhookEventType = Literal['checkout.created', 'checkout.updated', 'checkout.expired', 'customer.created', 'customer.updated', 'customer.deleted', 'customer.state_changed', 'customer_seat.assigned', 'customer_seat.claimed', 'customer_seat.revoked', 'member.created', 'member.updated', 'member.deleted', 'order.created', 'order.updated', 'order.paid', 'order.refunded', 'subscription.created', 'subscription.updated', 'subscription.active', 'subscription.canceled', 'subscription.uncanceled', 'subscription.revoked', 'subscription.past_due', 'refund.created', 'refund.updated', 'product.created', 'product.updated', 'benefit.created', 'benefit.updated', 'benefit_grant.created', 'benefit_grant.cycled', 'benefit_grant.updated', 'benefit_grant.revoked', 'organization.updated']
WebhookFormat = Literal['raw', 'discord', 'slack']
MetadataQuery = dict[str, Any] | None

class OrganizationsListQueryParams(TypedDict):
    slug: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[OrganizationSortProperty] | None]

class OrganizationsGetPathParams(TypedDict):
    id: str

class OrganizationsUpdatePathParams(TypedDict):
    id: str

class SubscriptionsListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    product_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    discount_id: NotRequired[str | list[str] | None]
    active: NotRequired[bool | None]
    cancel_at_period_end: NotRequired[bool | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[SubscriptionSortProperty] | None]
    metadata: NotRequired[MetadataQuery]

class SubscriptionsExportQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]

class SubscriptionsGetPathParams(TypedDict):
    id: str

class SubscriptionsUpdatePathParams(TypedDict):
    id: str

class SubscriptionsRevokePathParams(TypedDict):
    id: str

class Oauth2ClientsOauth2GetClientPathParams(TypedDict):
    client_id: str

class Oauth2ClientsOauth2UpdateClientPathParams(TypedDict):
    client_id: str

class Oauth2ClientsOauth2DeleteClientPathParams(TypedDict):
    client_id: str

class BenefitsListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    type: NotRequired[BenefitType | list[BenefitType] | None]
    id: NotRequired[str | list[str] | None]
    exclude_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[BenefitSortProperty] | None]
    metadata: NotRequired[MetadataQuery]

class BenefitsGetPathParams(TypedDict):
    id: str

class BenefitsUpdatePathParams(TypedDict):
    id: str

class BenefitsDeletePathParams(TypedDict):
    id: str

class BenefitsGrantsPathParams(TypedDict):
    id: str

class BenefitsGrantsQueryParams(TypedDict):
    is_granted: NotRequired[bool | None]
    customer_id: NotRequired[str | list[str] | None]
    member_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]

class BenefitGrantsListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    is_granted: NotRequired[bool | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[BenefitGrantSortProperty] | None]

class WebhooksListWebhookEndpointsQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]

class WebhooksGetWebhookEndpointPathParams(TypedDict):
    id: str

class WebhooksUpdateWebhookEndpointPathParams(TypedDict):
    id: str

class WebhooksDeleteWebhookEndpointPathParams(TypedDict):
    id: str

class WebhooksResetWebhookEndpointSecretPathParams(TypedDict):
    id: str

class WebhooksListWebhookDeliveriesQueryParams(TypedDict):
    endpoint_id: NotRequired[str | list[str] | None]
    start_timestamp: NotRequired[str | None]
    end_timestamp: NotRequired[str | None]
    succeeded: NotRequired[bool | None]
    query: NotRequired[str | None]
    http_code_class: NotRequired[Literal['2xx', '3xx', '4xx', '5xx'] | None]
    event_type: NotRequired[WebhookEventType | list[WebhookEventType] | None]
    page: NotRequired[int]
    limit: NotRequired[int]

class WebhooksRedeliverWebhookEventPathParams(TypedDict):
    id: str

class ProductsListQueryParams(TypedDict):
    id: NotRequired[str | list[str] | None]
    organization_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    is_archived: NotRequired[bool | None]
    is_recurring: NotRequired[bool | None]
    benefit_id: NotRequired[str | list[str] | None]
    visibility: NotRequired[list[ProductVisibility] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[ProductSortProperty] | None]
    metadata: NotRequired[MetadataQuery]

class ProductsGetPathParams(TypedDict):
    id: str

class ProductsUpdatePathParams(TypedDict):
    id: str

class ProductsUpdateBenefitsPathParams(TypedDict):
    id: str

class OrdersListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    product_id: NotRequired[str | list[str] | None]
    product_billing_type: NotRequired[ProductBillingType | list[ProductBillingType] | None]
    discount_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    checkout_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[OrderSortProperty] | None]
    metadata: NotRequired[MetadataQuery]

class OrdersExportQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    product_id: NotRequired[str | list[str] | None]

class OrdersGetPathParams(TypedDict):
    id: str

class OrdersUpdatePathParams(TypedDict):
    id: str

class OrdersInvoicePathParams(TypedDict):
    id: str

class OrdersGenerateInvoicePathParams(TypedDict):
    id: str

class RefundsListQueryParams(TypedDict):
    id: NotRequired[str | list[str] | None]
    organization_id: NotRequired[str | list[str] | None]
    order_id: NotRequired[str | list[str] | None]
    subscription_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    succeeded: NotRequired[bool | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[RefundSortProperty] | None]

class DisputesListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    order_id: NotRequired[str | list[str] | None]
    status: NotRequired[DisputeStatus | list[DisputeStatus] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[DisputeSortProperty] | None]

class DisputesGetPathParams(TypedDict):
    id: str

class CheckoutsListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    product_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    status: NotRequired[CheckoutStatus | list[CheckoutStatus] | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CheckoutSortProperty] | None]

class CheckoutsGetPathParams(TypedDict):
    id: str

class CheckoutsUpdatePathParams(TypedDict):
    id: str

class CheckoutsClientGetPathParams(TypedDict):
    client_secret: str

class CheckoutsClientUpdatePathParams(TypedDict):
    client_secret: str

class CheckoutsClientConfirmPathParams(TypedDict):
    client_secret: str

class FilesListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    ids: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]

class FilesUploadedPathParams(TypedDict):
    id: str

class FilesUpdatePathParams(TypedDict):
    id: str

class FilesDeletePathParams(TypedDict):
    id: str

class MetricsGetQueryParams(TypedDict):
    start_date: str
    end_date: str
    timezone: NotRequired[Literal['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', 'Africa/Algiers', 'Africa/Asmara', 'Africa/Asmera', 'Africa/Bamako', 'Africa/Bangui', 'Africa/Banjul', 'Africa/Bissau', 'Africa/Blantyre', 'Africa/Brazzaville', 'Africa/Bujumbura', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/Conakry', 'Africa/Dakar', 'Africa/Dar_es_Salaam', 'Africa/Djibouti', 'Africa/Douala', 'Africa/El_Aaiun', 'Africa/Freetown', 'Africa/Gaborone', 'Africa/Harare', 'Africa/Johannesburg', 'Africa/Juba', 'Africa/Kampala', 'Africa/Khartoum', 'Africa/Kigali', 'Africa/Kinshasa', 'Africa/Lagos', 'Africa/Libreville', 'Africa/Lome', 'Africa/Luanda', 'Africa/Lubumbashi', 'Africa/Lusaka', 'Africa/Malabo', 'Africa/Maputo', 'Africa/Maseru', 'Africa/Mbabane', 'Africa/Mogadishu', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Niamey', 'Africa/Nouakchott', 'Africa/Ouagadougou', 'Africa/Porto-Novo', 'Africa/Sao_Tome', 'Africa/Timbuktu', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Anguilla', 'America/Antigua', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/ComodRivadavia', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Aruba', 'America/Asuncion', 'America/Atikokan', 'America/Atka', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Buenos_Aires', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Catamarca', 'America/Cayenne', 'America/Cayman', 'America/Chicago', 'America/Chihuahua', 'America/Ciudad_Juarez', 'America/Coral_Harbour', 'America/Cordoba', 'America/Costa_Rica', 'America/Coyhaique', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Dominica', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Ensenada', 'America/Fort_Nelson', 'America/Fort_Wayne', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Grenada', 'America/Guadeloupe', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Indianapolis', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Jujuy', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Knox_IN', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Mendoza', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Rosario', 'America/Santa_Isabel', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Shiprock', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Virgin', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/South_Pole', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Ashkhabad', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Calcutta', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Chongqing', 'Asia/Chungking', 'Asia/Colombo', 'Asia/Dacca', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Harbin', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kashgar', 'Asia/Kathmandu', 'Asia/Katmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macao', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Rangoon', 'Asia/Riyadh', 'Asia/Saigon', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Tel_Aviv', 'Asia/Thimbu', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ujung_Pandang', 'Asia/Ulaanbaatar', 'Asia/Ulan_Bator', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faeroe', 'Atlantic/Faroe', 'Atlantic/Jan_Mayen', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/ACT', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Canberra', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/LHI', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/NSW', 'Australia/North', 'Australia/Perth', 'Australia/Queensland', 'Australia/South', 'Australia/Sydney', 'Australia/Tasmania', 'Australia/Victoria', 'Australia/West', 'Australia/Yancowinna', 'Brazil/Acre', 'Brazil/DeNoronha', 'Brazil/East', 'Brazil/West', 'CET', 'CST6CDT', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Canada/Saskatchewan', 'Canada/Yukon', 'Chile/Continental', 'Chile/EasterIsland', 'Cuba', 'EET', 'EST', 'EST5EDT', 'Egypt', 'Eire', 'Etc/GMT', 'Etc/GMT+0', 'Etc/GMT+1', 'Etc/GMT+10', 'Etc/GMT+11', 'Etc/GMT+12', 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5', 'Etc/GMT+6', 'Etc/GMT+7', 'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT-0', 'Etc/GMT-1', 'Etc/GMT-10', 'Etc/GMT-11', 'Etc/GMT-12', 'Etc/GMT-13', 'Etc/GMT-14', 'Etc/GMT-2', 'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5', 'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8', 'Etc/GMT-9', 'Etc/GMT0', 'Etc/Greenwich', 'Etc/UCT', 'Etc/UTC', 'Etc/Universal', 'Etc/Zulu', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belfast', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Kyiv', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Nicosia', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Tiraspol', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'Factory', 'GB', 'GB-Eire', 'GMT', 'GMT+0', 'GMT-0', 'GMT0', 'Greenwich', 'HST', 'Hongkong', 'Iceland', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Iran', 'Israel', 'Jamaica', 'Japan', 'Kwajalein', 'Libya', 'MET', 'MST', 'MST7MDT', 'Mexico/BajaNorte', 'Mexico/BajaSur', 'Mexico/General', 'NZ', 'NZ-CHAT', 'Navajo', 'PRC', 'PST8PDT', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Johnston', 'Pacific/Kanton', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Ponape', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Samoa', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Truk', 'Pacific/Wake', 'Pacific/Wallis', 'Pacific/Yap', 'Poland', 'Portugal', 'ROC', 'ROK', 'Singapore', 'Turkey', 'UCT', 'US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central', 'US/East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', 'US/Samoa', 'UTC', 'Universal', 'W-SU', 'WET', 'Zulu', 'localtime']]
    interval: TimeInterval
    organization_id: NotRequired[str | list[str] | None]
    product_id: NotRequired[str | list[str] | None]
    billing_type: NotRequired[ProductBillingType | list[ProductBillingType] | None]
    customer_id: NotRequired[str | list[str] | None]
    metrics: NotRequired[list[str] | None]

class LicenseKeysListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    benefit_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]

class LicenseKeysGetPathParams(TypedDict):
    id: str

class LicenseKeysUpdatePathParams(TypedDict):
    id: str

class LicenseKeysGetActivationPathParams(TypedDict):
    id: str
    activation_id: str

class CheckoutLinksListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    product_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CheckoutLinkSortProperty] | None]

class CheckoutLinksGetPathParams(TypedDict):
    id: str

class CheckoutLinksUpdatePathParams(TypedDict):
    id: str

class CheckoutLinksDeletePathParams(TypedDict):
    id: str

class CustomFieldsListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    type: NotRequired[CustomFieldType | list[CustomFieldType] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomFieldSortProperty] | None]

class CustomFieldsGetPathParams(TypedDict):
    id: str

class CustomFieldsUpdatePathParams(TypedDict):
    id: str

class CustomFieldsDeletePathParams(TypedDict):
    id: str

class DiscountsListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[DiscountSortProperty] | None]

class DiscountsGetPathParams(TypedDict):
    id: str

class DiscountsUpdatePathParams(TypedDict):
    id: str

class DiscountsDeletePathParams(TypedDict):
    id: str

class CustomersListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    email: NotRequired[str | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomerSortProperty] | None]
    metadata: NotRequired[MetadataQuery]

class CustomersExportQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]

class CustomersGetPathParams(TypedDict):
    id: str

class CustomersUpdatePathParams(TypedDict):
    id: str

class CustomersDeletePathParams(TypedDict):
    id: str

class CustomersDeleteQueryParams(TypedDict):
    anonymize: NotRequired[bool]

class CustomersGetExternalPathParams(TypedDict):
    external_id: str

class CustomersUpdateExternalPathParams(TypedDict):
    external_id: str

class CustomersDeleteExternalPathParams(TypedDict):
    external_id: str

class CustomersDeleteExternalQueryParams(TypedDict):
    anonymize: NotRequired[bool]

class CustomersGetStatePathParams(TypedDict):
    id: str

class CustomersGetStateExternalPathParams(TypedDict):
    external_id: str

class MembersListMembersQueryParams(TypedDict):
    customer_id: NotRequired[str | None]
    external_customer_id: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[MemberSortProperty] | None]

class MembersGetMemberPathParams(TypedDict):
    id: str

class MembersUpdateMemberPathParams(TypedDict):
    id: str

class MembersDeleteMemberPathParams(TypedDict):
    id: str

class CustomerPortalBenefitGrantsListQueryParams(TypedDict):
    query: NotRequired[str | None]
    type: NotRequired[BenefitType | list[BenefitType] | None]
    benefit_id: NotRequired[str | list[str] | None]
    checkout_id: NotRequired[str | list[str] | None]
    order_id: NotRequired[str | list[str] | None]
    subscription_id: NotRequired[str | list[str] | None]
    member_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomerBenefitGrantSortProperty] | None]

class CustomerPortalBenefitGrantsGetPathParams(TypedDict):
    id: str

class CustomerPortalBenefitGrantsUpdatePathParams(TypedDict):
    id: str

class CustomerPortalCustomersListPaymentMethodsQueryParams(TypedDict):
    page: NotRequired[int]
    limit: NotRequired[int]

class CustomerPortalCustomersDeletePaymentMethodPathParams(TypedDict):
    id: str

class CustomerPortalCustomerMetersListQueryParams(TypedDict):
    meter_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomerCustomerMeterSortProperty] | None]

class CustomerPortalCustomerMetersGetPathParams(TypedDict):
    id: str

class CustomerPortalSeatsListSeatsQueryParams(TypedDict):
    subscription_id: NotRequired[str | None]
    order_id: NotRequired[str | None]

class CustomerPortalSeatsRevokeSeatPathParams(TypedDict):
    seat_id: str

class CustomerPortalSeatsResendInvitationPathParams(TypedDict):
    seat_id: str

class CustomerPortalDownloadablesListQueryParams(TypedDict):
    benefit_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]

class CustomerPortalLicenseKeysListQueryParams(TypedDict):
    benefit_id: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]

class CustomerPortalLicenseKeysGetPathParams(TypedDict):
    id: str

class CustomerPortalMembersUpdateMemberPathParams(TypedDict):
    id: str

class CustomerPortalMembersRemoveMemberPathParams(TypedDict):
    id: str

class CustomerPortalOrdersListQueryParams(TypedDict):
    product_id: NotRequired[str | list[str] | None]
    product_billing_type: NotRequired[ProductBillingType | list[ProductBillingType] | None]
    subscription_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomerOrderSortProperty] | None]

class CustomerPortalOrdersGetPathParams(TypedDict):
    id: str

class CustomerPortalOrdersUpdatePathParams(TypedDict):
    id: str

class CustomerPortalOrdersInvoicePathParams(TypedDict):
    id: str

class CustomerPortalOrdersGenerateInvoicePathParams(TypedDict):
    id: str

class CustomerPortalOrdersGetPaymentStatusPathParams(TypedDict):
    id: str

class CustomerPortalOrdersConfirmRetryPaymentPathParams(TypedDict):
    id: str

class CustomerPortalOrganizationsGetPathParams(TypedDict):
    slug: str

class CustomerPortalSubscriptionsListQueryParams(TypedDict):
    product_id: NotRequired[str | list[str] | None]
    active: NotRequired[bool | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomerSubscriptionSortProperty] | None]

class CustomerPortalSubscriptionsGetPathParams(TypedDict):
    id: str

class CustomerPortalSubscriptionsUpdatePathParams(TypedDict):
    id: str

class CustomerPortalSubscriptionsCancelPathParams(TypedDict):
    id: str

class CustomerPortalWalletsListQueryParams(TypedDict):
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomerWalletSortProperty] | None]

class CustomerPortalWalletsGetPathParams(TypedDict):
    id: str

class CustomerSeatsListSeatsQueryParams(TypedDict):
    subscription_id: NotRequired[str | None]
    order_id: NotRequired[str | None]

class CustomerSeatsRevokeSeatPathParams(TypedDict):
    seat_id: str

class CustomerSeatsResendInvitationPathParams(TypedDict):
    seat_id: str

class CustomerSeatsGetClaimInfoPathParams(TypedDict):
    invitation_token: str

class EventsListQueryParams(TypedDict):
    filter: NotRequired[str | None]
    start_timestamp: NotRequired[str | None]
    end_timestamp: NotRequired[str | None]
    organization_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    meter_id: NotRequired[str | None]
    name: NotRequired[str | list[str] | None]
    source: NotRequired[EventSource | list[EventSource] | None]
    query: NotRequired[str | None]
    parent_id: NotRequired[str | None]
    depth: NotRequired[int | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[EventSortProperty] | None]
    metadata: NotRequired[MetadataQuery]

class EventsListNamesQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    source: NotRequired[EventSource | list[EventSource] | None]
    query: NotRequired[str | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[EventNamesSortProperty] | None]

class EventsGetPathParams(TypedDict):
    id: str

class EventTypesListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    root_events: NotRequired[bool]
    parent_id: NotRequired[str | None]
    source: NotRequired[EventSource | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[EventTypesSortProperty] | None]

class EventTypesUpdatePathParams(TypedDict):
    id: str

class MetersListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    query: NotRequired[str | None]
    is_archived: NotRequired[bool | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[MeterSortProperty] | None]
    metadata: NotRequired[MetadataQuery]

class MetersGetPathParams(TypedDict):
    id: str

class MetersUpdatePathParams(TypedDict):
    id: str

class MetersQuantitiesPathParams(TypedDict):
    id: str

class MetersQuantitiesQueryParams(TypedDict):
    start_timestamp: str
    end_timestamp: str
    interval: TimeInterval
    timezone: NotRequired[Literal['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', 'Africa/Algiers', 'Africa/Asmara', 'Africa/Asmera', 'Africa/Bamako', 'Africa/Bangui', 'Africa/Banjul', 'Africa/Bissau', 'Africa/Blantyre', 'Africa/Brazzaville', 'Africa/Bujumbura', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/Conakry', 'Africa/Dakar', 'Africa/Dar_es_Salaam', 'Africa/Djibouti', 'Africa/Douala', 'Africa/El_Aaiun', 'Africa/Freetown', 'Africa/Gaborone', 'Africa/Harare', 'Africa/Johannesburg', 'Africa/Juba', 'Africa/Kampala', 'Africa/Khartoum', 'Africa/Kigali', 'Africa/Kinshasa', 'Africa/Lagos', 'Africa/Libreville', 'Africa/Lome', 'Africa/Luanda', 'Africa/Lubumbashi', 'Africa/Lusaka', 'Africa/Malabo', 'Africa/Maputo', 'Africa/Maseru', 'Africa/Mbabane', 'Africa/Mogadishu', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Niamey', 'Africa/Nouakchott', 'Africa/Ouagadougou', 'Africa/Porto-Novo', 'Africa/Sao_Tome', 'Africa/Timbuktu', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Anguilla', 'America/Antigua', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/ComodRivadavia', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Aruba', 'America/Asuncion', 'America/Atikokan', 'America/Atka', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Buenos_Aires', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Catamarca', 'America/Cayenne', 'America/Cayman', 'America/Chicago', 'America/Chihuahua', 'America/Ciudad_Juarez', 'America/Coral_Harbour', 'America/Cordoba', 'America/Costa_Rica', 'America/Coyhaique', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Dominica', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Ensenada', 'America/Fort_Nelson', 'America/Fort_Wayne', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Grenada', 'America/Guadeloupe', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Indianapolis', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Jujuy', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Knox_IN', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Mendoza', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Rosario', 'America/Santa_Isabel', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Shiprock', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Virgin', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/South_Pole', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Ashkhabad', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Calcutta', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Chongqing', 'Asia/Chungking', 'Asia/Colombo', 'Asia/Dacca', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Harbin', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kashgar', 'Asia/Kathmandu', 'Asia/Katmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macao', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Rangoon', 'Asia/Riyadh', 'Asia/Saigon', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Tel_Aviv', 'Asia/Thimbu', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ujung_Pandang', 'Asia/Ulaanbaatar', 'Asia/Ulan_Bator', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faeroe', 'Atlantic/Faroe', 'Atlantic/Jan_Mayen', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/ACT', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Canberra', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/LHI', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/NSW', 'Australia/North', 'Australia/Perth', 'Australia/Queensland', 'Australia/South', 'Australia/Sydney', 'Australia/Tasmania', 'Australia/Victoria', 'Australia/West', 'Australia/Yancowinna', 'Brazil/Acre', 'Brazil/DeNoronha', 'Brazil/East', 'Brazil/West', 'CET', 'CST6CDT', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Canada/Saskatchewan', 'Canada/Yukon', 'Chile/Continental', 'Chile/EasterIsland', 'Cuba', 'EET', 'EST', 'EST5EDT', 'Egypt', 'Eire', 'Etc/GMT', 'Etc/GMT+0', 'Etc/GMT+1', 'Etc/GMT+10', 'Etc/GMT+11', 'Etc/GMT+12', 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5', 'Etc/GMT+6', 'Etc/GMT+7', 'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT-0', 'Etc/GMT-1', 'Etc/GMT-10', 'Etc/GMT-11', 'Etc/GMT-12', 'Etc/GMT-13', 'Etc/GMT-14', 'Etc/GMT-2', 'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5', 'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8', 'Etc/GMT-9', 'Etc/GMT0', 'Etc/Greenwich', 'Etc/UCT', 'Etc/UTC', 'Etc/Universal', 'Etc/Zulu', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belfast', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Kyiv', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Nicosia', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Tiraspol', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'Factory', 'GB', 'GB-Eire', 'GMT', 'GMT+0', 'GMT-0', 'GMT0', 'Greenwich', 'HST', 'Hongkong', 'Iceland', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Iran', 'Israel', 'Jamaica', 'Japan', 'Kwajalein', 'Libya', 'MET', 'MST', 'MST7MDT', 'Mexico/BajaNorte', 'Mexico/BajaSur', 'Mexico/General', 'NZ', 'NZ-CHAT', 'Navajo', 'PRC', 'PST8PDT', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Johnston', 'Pacific/Kanton', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Ponape', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Samoa', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Truk', 'Pacific/Wake', 'Pacific/Wallis', 'Pacific/Yap', 'Poland', 'Portugal', 'ROC', 'ROK', 'Singapore', 'Turkey', 'UCT', 'US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central', 'US/East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', 'US/Samoa', 'UTC', 'Universal', 'W-SU', 'WET', 'Zulu', 'localtime']]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    customer_aggregation_function: NotRequired[AggregationFunction | None]
    metadata: NotRequired[MetadataQuery]

class OrganizationAccessTokensListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[OrganizationAccessTokenSortProperty] | None]

class OrganizationAccessTokensUpdatePathParams(TypedDict):
    id: str

class OrganizationAccessTokensDeletePathParams(TypedDict):
    id: str

class CustomerMetersListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    customer_id: NotRequired[str | list[str] | None]
    external_customer_id: NotRequired[str | list[str] | None]
    meter_id: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[CustomerMeterSortProperty] | None]

class CustomerMetersGetPathParams(TypedDict):
    id: str

class PaymentsListQueryParams(TypedDict):
    organization_id: NotRequired[str | list[str] | None]
    checkout_id: NotRequired[str | list[str] | None]
    order_id: NotRequired[str | list[str] | None]
    status: NotRequired[PaymentStatus | list[PaymentStatus] | None]
    method: NotRequired[str | list[str] | None]
    customer_email: NotRequired[str | list[str] | None]
    page: NotRequired[int]
    limit: NotRequired[int]
    sorting: NotRequired[list[PaymentSortProperty] | None]

class PaymentsGetPathParams(TypedDict):
    id: str

class BaseClient:

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/organizations/'], *, query_params: OrganizationsListQueryParams=...) -> ListResource_Organization_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/organizations/'], *, body: OrganizationCreate) -> Organization:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/organizations/{id}'], *, path_params: OrganizationsGetPathParams) -> Organization:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/organizations/{id}'], *, path_params: OrganizationsUpdatePathParams, body: OrganizationUpdate) -> Organization:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/subscriptions/'], *, query_params: SubscriptionsListQueryParams=...) -> ListResource_Subscription_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/subscriptions/'], *, body: SubscriptionCreateCustomer | SubscriptionCreateExternalCustomer) -> Subscription:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/subscriptions/export'], *, query_params: SubscriptionsExportQueryParams=...) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/subscriptions/{id}'], *, path_params: SubscriptionsGetPathParams) -> Subscription:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/subscriptions/{id}'], *, path_params: SubscriptionsUpdatePathParams, body: SubscriptionUpdate) -> Subscription:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/subscriptions/{id}'], *, path_params: SubscriptionsRevokePathParams) -> Subscription:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/register'], *, body: OAuth2ClientConfiguration) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/oauth2/register/{client_id}'], *, path_params: Oauth2ClientsOauth2GetClientPathParams) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['PUT'], path: Literal['/v1/oauth2/register/{client_id}'], *, path_params: Oauth2ClientsOauth2UpdateClientPathParams, body: OAuth2ClientConfigurationUpdate) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/oauth2/register/{client_id}'], *, path_params: Oauth2ClientsOauth2DeleteClientPathParams) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/oauth2/authorize']) -> AuthorizeResponseUser | AuthorizeResponseOrganization:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/token']) -> TokenResponse:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/revoke']) -> RevokeTokenResponse:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/introspect']) -> IntrospectTokenResponse:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/oauth2/userinfo']) -> UserInfoUser | UserInfoOrganization:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/benefits/'], *, query_params: BenefitsListQueryParams=...) -> ListResource_Benefit_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/benefits/'], *, body: BenefitCreate) -> Benefit:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/benefits/{id}'], *, path_params: BenefitsGetPathParams) -> Benefit:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/benefits/{id}'], *, path_params: BenefitsUpdatePathParams, body: BenefitCustomUpdate | BenefitDiscordUpdate | BenefitGitHubRepositoryUpdate | BenefitDownloadablesUpdate | BenefitLicenseKeysUpdate | BenefitMeterCreditUpdate) -> Benefit:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/benefits/{id}'], *, path_params: BenefitsDeletePathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/benefits/{id}/grants'], *, path_params: BenefitsGrantsPathParams, query_params: BenefitsGrantsQueryParams=...) -> ListResource_BenefitGrant_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/benefit-grants/'], *, query_params: BenefitGrantsListQueryParams=...) -> ListResource_BenefitGrant_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/webhooks/endpoints'], *, query_params: WebhooksListWebhookEndpointsQueryParams=...) -> ListResource_WebhookEndpoint_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/webhooks/endpoints'], *, body: WebhookEndpointCreate) -> WebhookEndpoint:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/webhooks/endpoints/{id}'], *, path_params: WebhooksGetWebhookEndpointPathParams) -> WebhookEndpoint:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/webhooks/endpoints/{id}'], *, path_params: WebhooksUpdateWebhookEndpointPathParams, body: WebhookEndpointUpdate) -> WebhookEndpoint:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/webhooks/endpoints/{id}'], *, path_params: WebhooksDeleteWebhookEndpointPathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/webhooks/endpoints/{id}/secret'], *, path_params: WebhooksResetWebhookEndpointSecretPathParams) -> WebhookEndpoint:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/webhooks/deliveries'], *, query_params: WebhooksListWebhookDeliveriesQueryParams=...) -> ListResource_WebhookDelivery_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/webhooks/events/{id}/redeliver'], *, path_params: WebhooksRedeliverWebhookEventPathParams) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/products/'], *, query_params: ProductsListQueryParams=...) -> ListResource_Product_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/products/'], *, body: ProductCreate) -> Product:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/products/{id}'], *, path_params: ProductsGetPathParams) -> Product:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/products/{id}'], *, path_params: ProductsUpdatePathParams, body: ProductUpdate) -> Product:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/products/{id}/benefits'], *, path_params: ProductsUpdateBenefitsPathParams, body: ProductBenefitsUpdate) -> Product:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/'], *, query_params: OrdersListQueryParams=...) -> ListResource_Order_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/export'], *, query_params: OrdersExportQueryParams=...) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/{id}'], *, path_params: OrdersGetPathParams) -> Order:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/orders/{id}'], *, path_params: OrdersUpdatePathParams, body: OrderUpdate) -> Order:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/{id}/invoice'], *, path_params: OrdersInvoicePathParams) -> OrderInvoice:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/orders/{id}/invoice'], *, path_params: OrdersGenerateInvoicePathParams) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/refunds/'], *, query_params: RefundsListQueryParams=...) -> ListResource_Refund_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/refunds/'], *, body: RefundCreate) -> Refund:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/disputes/'], *, query_params: DisputesListQueryParams=...) -> ListResource_Dispute_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/disputes/{id}'], *, path_params: DisputesGetPathParams) -> Dispute:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/checkouts/'], *, query_params: CheckoutsListQueryParams=...) -> ListResource_Checkout_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/checkouts/'], *, body: CheckoutCreate) -> Checkout:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/checkouts/{id}'], *, path_params: CheckoutsGetPathParams) -> Checkout:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/checkouts/{id}'], *, path_params: CheckoutsUpdatePathParams, body: CheckoutUpdate) -> Checkout:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/checkouts/client/{client_secret}'], *, path_params: CheckoutsClientGetPathParams) -> CheckoutPublic:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/checkouts/client/{client_secret}'], *, path_params: CheckoutsClientUpdatePathParams, body: CheckoutUpdatePublic) -> CheckoutPublic:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/checkouts/client/{client_secret}/confirm'], *, path_params: CheckoutsClientConfirmPathParams, body: CheckoutConfirmStripe) -> CheckoutPublicConfirmed:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/files/'], *, query_params: FilesListQueryParams=...) -> ListResource_FileRead_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/files/'], *, body: FileCreate) -> FileUpload:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/files/{id}/uploaded'], *, path_params: FilesUploadedPathParams, body: FileUploadCompleted) -> DownloadableFileRead | ProductMediaFileRead | OrganizationAvatarFileRead:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/files/{id}'], *, path_params: FilesUpdatePathParams, body: FilePatch) -> DownloadableFileRead | ProductMediaFileRead | OrganizationAvatarFileRead:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/files/{id}'], *, path_params: FilesDeletePathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/metrics/'], *, query_params: MetricsGetQueryParams) -> MetricsResponse:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/metrics/limits']) -> MetricsLimits:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/license-keys/'], *, query_params: LicenseKeysListQueryParams=...) -> ListResource_LicenseKeyRead_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/license-keys/{id}'], *, path_params: LicenseKeysGetPathParams) -> LicenseKeyWithActivations:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/license-keys/{id}'], *, path_params: LicenseKeysUpdatePathParams, body: LicenseKeyUpdate) -> LicenseKeyRead:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/license-keys/{id}/activations/{activation_id}'], *, path_params: LicenseKeysGetActivationPathParams) -> LicenseKeyActivationRead:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/license-keys/validate'], *, body: LicenseKeyValidate) -> ValidatedLicenseKey:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/license-keys/activate'], *, body: LicenseKeyActivate) -> LicenseKeyActivationRead:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/license-keys/deactivate'], *, body: LicenseKeyDeactivate) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/checkout-links/'], *, query_params: CheckoutLinksListQueryParams=...) -> ListResource_CheckoutLink_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/checkout-links/'], *, body: CheckoutLinkCreate) -> CheckoutLink:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/checkout-links/{id}'], *, path_params: CheckoutLinksGetPathParams) -> CheckoutLink:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/checkout-links/{id}'], *, path_params: CheckoutLinksUpdatePathParams, body: CheckoutLinkUpdate) -> CheckoutLink:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/checkout-links/{id}'], *, path_params: CheckoutLinksDeletePathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/custom-fields/'], *, query_params: CustomFieldsListQueryParams=...) -> ListResource_CustomField_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/custom-fields/'], *, body: CustomFieldCreate) -> CustomField:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/custom-fields/{id}'], *, path_params: CustomFieldsGetPathParams) -> CustomField:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/custom-fields/{id}'], *, path_params: CustomFieldsUpdatePathParams, body: CustomFieldUpdate) -> CustomField:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/custom-fields/{id}'], *, path_params: CustomFieldsDeletePathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/discounts/'], *, query_params: DiscountsListQueryParams=...) -> ListResource_Discount_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/discounts/'], *, body: DiscountCreate) -> Discount:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/discounts/{id}'], *, path_params: DiscountsGetPathParams) -> Discount:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/discounts/{id}'], *, path_params: DiscountsUpdatePathParams, body: DiscountUpdate) -> Discount:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/discounts/{id}'], *, path_params: DiscountsDeletePathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/'], *, query_params: CustomersListQueryParams=...) -> ListResource_CustomerWithMembers_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customers/'], *, body: CustomerCreate) -> CustomerWithMembers:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/export'], *, query_params: CustomersExportQueryParams=...) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/{id}'], *, path_params: CustomersGetPathParams) -> CustomerWithMembers:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customers/{id}'], *, path_params: CustomersUpdatePathParams, body: CustomerUpdate) -> CustomerWithMembers:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customers/{id}'], *, path_params: CustomersDeletePathParams, query_params: CustomersDeleteQueryParams=...) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/external/{external_id}'], *, path_params: CustomersGetExternalPathParams) -> CustomerWithMembers:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customers/external/{external_id}'], *, path_params: CustomersUpdateExternalPathParams, body: CustomerUpdateExternalID) -> CustomerWithMembers:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customers/external/{external_id}'], *, path_params: CustomersDeleteExternalPathParams, query_params: CustomersDeleteExternalQueryParams=...) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/{id}/state'], *, path_params: CustomersGetStatePathParams) -> CustomerState:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/external/{external_id}/state'], *, path_params: CustomersGetStateExternalPathParams) -> CustomerState:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/members/'], *, query_params: MembersListMembersQueryParams=...) -> ListResource_Member_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/members/'], *, body: MemberCreate) -> Member:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/members/{id}'], *, path_params: MembersGetMemberPathParams) -> Member:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/members/{id}'], *, path_params: MembersUpdateMemberPathParams, body: MemberUpdate) -> Member:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/members/{id}'], *, path_params: MembersDeleteMemberPathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/benefit-grants/'], *, query_params: CustomerPortalBenefitGrantsListQueryParams=...) -> ListResource_CustomerBenefitGrant_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/benefit-grants/{id}'], *, path_params: CustomerPortalBenefitGrantsGetPathParams) -> CustomerBenefitGrant:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/benefit-grants/{id}'], *, path_params: CustomerPortalBenefitGrantsUpdatePathParams, body: CustomerBenefitGrantUpdate) -> CustomerBenefitGrant:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customers/me']) -> CustomerPortalCustomer:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/customers/me'], *, body: CustomerPortalCustomerUpdate) -> CustomerPortalCustomer:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customers/me/payment-methods'], *, query_params: CustomerPortalCustomersListPaymentMethodsQueryParams=...) -> ListResource_CustomerPaymentMethod_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/customers/me/payment-methods'], *, body: CustomerPaymentMethodCreate) -> CustomerPaymentMethodCreateResponse:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/customers/me/payment-methods/confirm'], *, body: CustomerPaymentMethodConfirm) -> CustomerPaymentMethodCreateResponse:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/customers/me/payment-methods/{id}'], *, path_params: CustomerPortalCustomersDeletePaymentMethodPathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/meters/'], *, query_params: CustomerPortalCustomerMetersListQueryParams=...) -> ListResource_CustomerCustomerMeter_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/meters/{id}'], *, path_params: CustomerPortalCustomerMetersGetPathParams) -> CustomerCustomerMeter:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/seats'], *, query_params: CustomerPortalSeatsListSeatsQueryParams=...) -> SeatsList:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/seats'], *, body: SeatAssign) -> CustomerSeat:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/seats/{seat_id}'], *, path_params: CustomerPortalSeatsRevokeSeatPathParams) -> CustomerSeat:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/seats/{seat_id}/resend'], *, path_params: CustomerPortalSeatsResendInvitationPathParams) -> CustomerSeat:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/seats/subscriptions']) -> list[CustomerSubscription]:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customer-session/introspect']) -> CustomerCustomerSession:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customer-session/user']) -> PortalAuthenticatedUser:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/downloadables/'], *, query_params: CustomerPortalDownloadablesListQueryParams=...) -> ListResource_DownloadableRead_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/license-keys/'], *, query_params: CustomerPortalLicenseKeysListQueryParams=...) -> ListResource_LicenseKeyRead_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/license-keys/{id}'], *, path_params: CustomerPortalLicenseKeysGetPathParams) -> LicenseKeyWithActivations:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/license-keys/validate'], *, body: LicenseKeyValidate) -> ValidatedLicenseKey:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/license-keys/activate'], *, body: LicenseKeyActivate) -> LicenseKeyActivationRead:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/license-keys/deactivate'], *, body: LicenseKeyDeactivate) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/members']) -> list[CustomerPortalMember]:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/members'], *, body: CustomerPortalMemberCreate) -> CustomerPortalMember:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/members/{id}'], *, path_params: CustomerPortalMembersUpdateMemberPathParams, body: CustomerPortalMemberUpdate) -> CustomerPortalMember:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/members/{id}'], *, path_params: CustomerPortalMembersRemoveMemberPathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/'], *, query_params: CustomerPortalOrdersListQueryParams=...) -> ListResource_CustomerOrder_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/{id}'], *, path_params: CustomerPortalOrdersGetPathParams) -> CustomerOrder:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/orders/{id}'], *, path_params: CustomerPortalOrdersUpdatePathParams, body: CustomerOrderUpdate) -> CustomerOrder:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/{id}/invoice'], *, path_params: CustomerPortalOrdersInvoicePathParams) -> CustomerOrderInvoice:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/orders/{id}/invoice'], *, path_params: CustomerPortalOrdersGenerateInvoicePathParams) -> Any:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/{id}/payment-status'], *, path_params: CustomerPortalOrdersGetPaymentStatusPathParams) -> CustomerOrderPaymentStatus:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/orders/{id}/confirm-payment'], *, path_params: CustomerPortalOrdersConfirmRetryPaymentPathParams, body: CustomerOrderConfirmPayment) -> CustomerOrderPaymentConfirmation:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/organizations/{slug}'], *, path_params: CustomerPortalOrganizationsGetPathParams) -> CustomerOrganizationData:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/subscriptions/'], *, query_params: CustomerPortalSubscriptionsListQueryParams=...) -> ListResource_CustomerSubscription_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/subscriptions/{id}'], *, path_params: CustomerPortalSubscriptionsGetPathParams) -> CustomerSubscription:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/subscriptions/{id}'], *, path_params: CustomerPortalSubscriptionsUpdatePathParams, body: CustomerSubscriptionUpdate) -> CustomerSubscription:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/subscriptions/{id}'], *, path_params: CustomerPortalSubscriptionsCancelPathParams) -> CustomerSubscription:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/wallets/'], *, query_params: CustomerPortalWalletsListQueryParams=...) -> ListResource_CustomerWallet_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/wallets/{id}'], *, path_params: CustomerPortalWalletsGetPathParams) -> CustomerWallet:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-seats'], *, query_params: CustomerSeatsListSeatsQueryParams=...) -> SeatsList:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-seats'], *, body: SeatAssign) -> CustomerSeat:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-seats/{seat_id}'], *, path_params: CustomerSeatsRevokeSeatPathParams) -> CustomerSeat:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-seats/{seat_id}/resend'], *, path_params: CustomerSeatsResendInvitationPathParams) -> CustomerSeat:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-seats/claim/{invitation_token}'], *, path_params: CustomerSeatsGetClaimInfoPathParams) -> SeatClaimInfo:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-seats/claim'], *, body: SeatClaim) -> CustomerSeatClaimResponse:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-sessions/'], *, body: CustomerSessionCustomerIDCreate | CustomerSessionCustomerExternalIDCreate) -> CustomerSession:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/member-sessions/'], *, body: MemberSessionCreate) -> MemberSession:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/events/'], *, query_params: EventsListQueryParams=...) -> ListResource_Event_ | ListResourceWithCursorPagination_Event_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/events/names'], *, query_params: EventsListNamesQueryParams=...) -> ListResource_EventName_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/events/{id}'], *, path_params: EventsGetPathParams) -> Event:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/events/ingest'], *, body: EventsIngest) -> EventsIngestResponse:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/event-types/'], *, query_params: EventTypesListQueryParams=...) -> ListResource_EventTypeWithStats_:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/event-types/{id}'], *, path_params: EventTypesUpdatePathParams, body: EventTypeUpdate) -> EventType:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/meters/'], *, query_params: MetersListQueryParams=...) -> ListResource_Meter_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/meters/'], *, body: MeterCreate) -> Meter:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/meters/{id}'], *, path_params: MetersGetPathParams) -> Meter:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/meters/{id}'], *, path_params: MetersUpdatePathParams, body: MeterUpdate) -> Meter:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/meters/{id}/quantities'], *, path_params: MetersQuantitiesPathParams, query_params: MetersQuantitiesQueryParams) -> MeterQuantities:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/organization-access-tokens/'], *, query_params: OrganizationAccessTokensListQueryParams=...) -> ListResource_OrganizationAccessToken_:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/v1/organization-access-tokens/'], *, body: OrganizationAccessTokenCreate) -> OrganizationAccessTokenCreateResponse:
        ...

    @overload
    def __call__(self, method: Literal['PATCH'], path: Literal['/v1/organization-access-tokens/{id}'], *, path_params: OrganizationAccessTokensUpdatePathParams, body: OrganizationAccessTokenUpdate) -> OrganizationAccessToken:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/v1/organization-access-tokens/{id}'], *, path_params: OrganizationAccessTokensDeletePathParams) -> None:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-meters/'], *, query_params: CustomerMetersListQueryParams=...) -> ListResource_CustomerMeter_:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-meters/{id}'], *, path_params: CustomerMetersGetPathParams) -> CustomerMeter:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/payments/'], *, query_params: PaymentsListQueryParams=...) -> ListResource__:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/v1/payments/{id}'], *, path_params: PaymentsGetPathParams) -> Payment:
        ...

    def __call__(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        return self.make_request(method, path, path_params=path_params, query_params=query_params, body=body)

    def make_request(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        raise NotImplementedError()

class AsyncBaseClient:

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/organizations/'], *, query_params: OrganizationsListQueryParams=...) -> ListResource_Organization_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/organizations/'], *, body: OrganizationCreate) -> Organization:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/organizations/{id}'], *, path_params: OrganizationsGetPathParams) -> Organization:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/organizations/{id}'], *, path_params: OrganizationsUpdatePathParams, body: OrganizationUpdate) -> Organization:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/subscriptions/'], *, query_params: SubscriptionsListQueryParams=...) -> ListResource_Subscription_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/subscriptions/'], *, body: SubscriptionCreateCustomer | SubscriptionCreateExternalCustomer) -> Subscription:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/subscriptions/export'], *, query_params: SubscriptionsExportQueryParams=...) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/subscriptions/{id}'], *, path_params: SubscriptionsGetPathParams) -> Subscription:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/subscriptions/{id}'], *, path_params: SubscriptionsUpdatePathParams, body: SubscriptionUpdate) -> Subscription:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/subscriptions/{id}'], *, path_params: SubscriptionsRevokePathParams) -> Subscription:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/register'], *, body: OAuth2ClientConfiguration) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/oauth2/register/{client_id}'], *, path_params: Oauth2ClientsOauth2GetClientPathParams) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['PUT'], path: Literal['/v1/oauth2/register/{client_id}'], *, path_params: Oauth2ClientsOauth2UpdateClientPathParams, body: OAuth2ClientConfigurationUpdate) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/oauth2/register/{client_id}'], *, path_params: Oauth2ClientsOauth2DeleteClientPathParams) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/oauth2/authorize']) -> AuthorizeResponseUser | AuthorizeResponseOrganization:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/token']) -> TokenResponse:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/revoke']) -> RevokeTokenResponse:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/oauth2/introspect']) -> IntrospectTokenResponse:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/oauth2/userinfo']) -> UserInfoUser | UserInfoOrganization:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/benefits/'], *, query_params: BenefitsListQueryParams=...) -> ListResource_Benefit_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/benefits/'], *, body: BenefitCreate) -> Benefit:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/benefits/{id}'], *, path_params: BenefitsGetPathParams) -> Benefit:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/benefits/{id}'], *, path_params: BenefitsUpdatePathParams, body: BenefitCustomUpdate | BenefitDiscordUpdate | BenefitGitHubRepositoryUpdate | BenefitDownloadablesUpdate | BenefitLicenseKeysUpdate | BenefitMeterCreditUpdate) -> Benefit:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/benefits/{id}'], *, path_params: BenefitsDeletePathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/benefits/{id}/grants'], *, path_params: BenefitsGrantsPathParams, query_params: BenefitsGrantsQueryParams=...) -> ListResource_BenefitGrant_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/benefit-grants/'], *, query_params: BenefitGrantsListQueryParams=...) -> ListResource_BenefitGrant_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/webhooks/endpoints'], *, query_params: WebhooksListWebhookEndpointsQueryParams=...) -> ListResource_WebhookEndpoint_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/webhooks/endpoints'], *, body: WebhookEndpointCreate) -> WebhookEndpoint:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/webhooks/endpoints/{id}'], *, path_params: WebhooksGetWebhookEndpointPathParams) -> WebhookEndpoint:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/webhooks/endpoints/{id}'], *, path_params: WebhooksUpdateWebhookEndpointPathParams, body: WebhookEndpointUpdate) -> WebhookEndpoint:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/webhooks/endpoints/{id}'], *, path_params: WebhooksDeleteWebhookEndpointPathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/webhooks/endpoints/{id}/secret'], *, path_params: WebhooksResetWebhookEndpointSecretPathParams) -> WebhookEndpoint:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/webhooks/deliveries'], *, query_params: WebhooksListWebhookDeliveriesQueryParams=...) -> ListResource_WebhookDelivery_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/webhooks/events/{id}/redeliver'], *, path_params: WebhooksRedeliverWebhookEventPathParams) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/products/'], *, query_params: ProductsListQueryParams=...) -> ListResource_Product_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/products/'], *, body: ProductCreate) -> Product:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/products/{id}'], *, path_params: ProductsGetPathParams) -> Product:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/products/{id}'], *, path_params: ProductsUpdatePathParams, body: ProductUpdate) -> Product:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/products/{id}/benefits'], *, path_params: ProductsUpdateBenefitsPathParams, body: ProductBenefitsUpdate) -> Product:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/'], *, query_params: OrdersListQueryParams=...) -> ListResource_Order_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/export'], *, query_params: OrdersExportQueryParams=...) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/{id}'], *, path_params: OrdersGetPathParams) -> Order:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/orders/{id}'], *, path_params: OrdersUpdatePathParams, body: OrderUpdate) -> Order:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/orders/{id}/invoice'], *, path_params: OrdersInvoicePathParams) -> OrderInvoice:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/orders/{id}/invoice'], *, path_params: OrdersGenerateInvoicePathParams) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/refunds/'], *, query_params: RefundsListQueryParams=...) -> ListResource_Refund_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/refunds/'], *, body: RefundCreate) -> Refund:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/disputes/'], *, query_params: DisputesListQueryParams=...) -> ListResource_Dispute_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/disputes/{id}'], *, path_params: DisputesGetPathParams) -> Dispute:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/checkouts/'], *, query_params: CheckoutsListQueryParams=...) -> ListResource_Checkout_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/checkouts/'], *, body: CheckoutCreate) -> Checkout:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/checkouts/{id}'], *, path_params: CheckoutsGetPathParams) -> Checkout:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/checkouts/{id}'], *, path_params: CheckoutsUpdatePathParams, body: CheckoutUpdate) -> Checkout:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/checkouts/client/{client_secret}'], *, path_params: CheckoutsClientGetPathParams) -> CheckoutPublic:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/checkouts/client/{client_secret}'], *, path_params: CheckoutsClientUpdatePathParams, body: CheckoutUpdatePublic) -> CheckoutPublic:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/checkouts/client/{client_secret}/confirm'], *, path_params: CheckoutsClientConfirmPathParams, body: CheckoutConfirmStripe) -> CheckoutPublicConfirmed:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/files/'], *, query_params: FilesListQueryParams=...) -> ListResource_FileRead_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/files/'], *, body: FileCreate) -> FileUpload:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/files/{id}/uploaded'], *, path_params: FilesUploadedPathParams, body: FileUploadCompleted) -> DownloadableFileRead | ProductMediaFileRead | OrganizationAvatarFileRead:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/files/{id}'], *, path_params: FilesUpdatePathParams, body: FilePatch) -> DownloadableFileRead | ProductMediaFileRead | OrganizationAvatarFileRead:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/files/{id}'], *, path_params: FilesDeletePathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/metrics/'], *, query_params: MetricsGetQueryParams) -> MetricsResponse:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/metrics/limits']) -> MetricsLimits:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/license-keys/'], *, query_params: LicenseKeysListQueryParams=...) -> ListResource_LicenseKeyRead_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/license-keys/{id}'], *, path_params: LicenseKeysGetPathParams) -> LicenseKeyWithActivations:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/license-keys/{id}'], *, path_params: LicenseKeysUpdatePathParams, body: LicenseKeyUpdate) -> LicenseKeyRead:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/license-keys/{id}/activations/{activation_id}'], *, path_params: LicenseKeysGetActivationPathParams) -> LicenseKeyActivationRead:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/license-keys/validate'], *, body: LicenseKeyValidate) -> ValidatedLicenseKey:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/license-keys/activate'], *, body: LicenseKeyActivate) -> LicenseKeyActivationRead:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/license-keys/deactivate'], *, body: LicenseKeyDeactivate) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/checkout-links/'], *, query_params: CheckoutLinksListQueryParams=...) -> ListResource_CheckoutLink_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/checkout-links/'], *, body: CheckoutLinkCreate) -> CheckoutLink:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/checkout-links/{id}'], *, path_params: CheckoutLinksGetPathParams) -> CheckoutLink:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/checkout-links/{id}'], *, path_params: CheckoutLinksUpdatePathParams, body: CheckoutLinkUpdate) -> CheckoutLink:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/checkout-links/{id}'], *, path_params: CheckoutLinksDeletePathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/custom-fields/'], *, query_params: CustomFieldsListQueryParams=...) -> ListResource_CustomField_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/custom-fields/'], *, body: CustomFieldCreate) -> CustomField:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/custom-fields/{id}'], *, path_params: CustomFieldsGetPathParams) -> CustomField:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/custom-fields/{id}'], *, path_params: CustomFieldsUpdatePathParams, body: CustomFieldUpdate) -> CustomField:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/custom-fields/{id}'], *, path_params: CustomFieldsDeletePathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/discounts/'], *, query_params: DiscountsListQueryParams=...) -> ListResource_Discount_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/discounts/'], *, body: DiscountCreate) -> Discount:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/discounts/{id}'], *, path_params: DiscountsGetPathParams) -> Discount:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/discounts/{id}'], *, path_params: DiscountsUpdatePathParams, body: DiscountUpdate) -> Discount:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/discounts/{id}'], *, path_params: DiscountsDeletePathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/'], *, query_params: CustomersListQueryParams=...) -> ListResource_CustomerWithMembers_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customers/'], *, body: CustomerCreate) -> CustomerWithMembers:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/export'], *, query_params: CustomersExportQueryParams=...) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/{id}'], *, path_params: CustomersGetPathParams) -> CustomerWithMembers:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customers/{id}'], *, path_params: CustomersUpdatePathParams, body: CustomerUpdate) -> CustomerWithMembers:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customers/{id}'], *, path_params: CustomersDeletePathParams, query_params: CustomersDeleteQueryParams=...) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/external/{external_id}'], *, path_params: CustomersGetExternalPathParams) -> CustomerWithMembers:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customers/external/{external_id}'], *, path_params: CustomersUpdateExternalPathParams, body: CustomerUpdateExternalID) -> CustomerWithMembers:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customers/external/{external_id}'], *, path_params: CustomersDeleteExternalPathParams, query_params: CustomersDeleteExternalQueryParams=...) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/{id}/state'], *, path_params: CustomersGetStatePathParams) -> CustomerState:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customers/external/{external_id}/state'], *, path_params: CustomersGetStateExternalPathParams) -> CustomerState:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/members/'], *, query_params: MembersListMembersQueryParams=...) -> ListResource_Member_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/members/'], *, body: MemberCreate) -> Member:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/members/{id}'], *, path_params: MembersGetMemberPathParams) -> Member:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/members/{id}'], *, path_params: MembersUpdateMemberPathParams, body: MemberUpdate) -> Member:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/members/{id}'], *, path_params: MembersDeleteMemberPathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/benefit-grants/'], *, query_params: CustomerPortalBenefitGrantsListQueryParams=...) -> ListResource_CustomerBenefitGrant_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/benefit-grants/{id}'], *, path_params: CustomerPortalBenefitGrantsGetPathParams) -> CustomerBenefitGrant:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/benefit-grants/{id}'], *, path_params: CustomerPortalBenefitGrantsUpdatePathParams, body: CustomerBenefitGrantUpdate) -> CustomerBenefitGrant:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customers/me']) -> CustomerPortalCustomer:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/customers/me'], *, body: CustomerPortalCustomerUpdate) -> CustomerPortalCustomer:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customers/me/payment-methods'], *, query_params: CustomerPortalCustomersListPaymentMethodsQueryParams=...) -> ListResource_CustomerPaymentMethod_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/customers/me/payment-methods'], *, body: CustomerPaymentMethodCreate) -> CustomerPaymentMethodCreateResponse:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/customers/me/payment-methods/confirm'], *, body: CustomerPaymentMethodConfirm) -> CustomerPaymentMethodCreateResponse:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/customers/me/payment-methods/{id}'], *, path_params: CustomerPortalCustomersDeletePaymentMethodPathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/meters/'], *, query_params: CustomerPortalCustomerMetersListQueryParams=...) -> ListResource_CustomerCustomerMeter_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/meters/{id}'], *, path_params: CustomerPortalCustomerMetersGetPathParams) -> CustomerCustomerMeter:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/seats'], *, query_params: CustomerPortalSeatsListSeatsQueryParams=...) -> SeatsList:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/seats'], *, body: SeatAssign) -> CustomerSeat:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/seats/{seat_id}'], *, path_params: CustomerPortalSeatsRevokeSeatPathParams) -> CustomerSeat:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/seats/{seat_id}/resend'], *, path_params: CustomerPortalSeatsResendInvitationPathParams) -> CustomerSeat:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/seats/subscriptions']) -> list[CustomerSubscription]:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customer-session/introspect']) -> CustomerCustomerSession:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/customer-session/user']) -> PortalAuthenticatedUser:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/downloadables/'], *, query_params: CustomerPortalDownloadablesListQueryParams=...) -> ListResource_DownloadableRead_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/license-keys/'], *, query_params: CustomerPortalLicenseKeysListQueryParams=...) -> ListResource_LicenseKeyRead_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/license-keys/{id}'], *, path_params: CustomerPortalLicenseKeysGetPathParams) -> LicenseKeyWithActivations:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/license-keys/validate'], *, body: LicenseKeyValidate) -> ValidatedLicenseKey:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/license-keys/activate'], *, body: LicenseKeyActivate) -> LicenseKeyActivationRead:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/license-keys/deactivate'], *, body: LicenseKeyDeactivate) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/members']) -> list[CustomerPortalMember]:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/members'], *, body: CustomerPortalMemberCreate) -> CustomerPortalMember:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/members/{id}'], *, path_params: CustomerPortalMembersUpdateMemberPathParams, body: CustomerPortalMemberUpdate) -> CustomerPortalMember:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/members/{id}'], *, path_params: CustomerPortalMembersRemoveMemberPathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/'], *, query_params: CustomerPortalOrdersListQueryParams=...) -> ListResource_CustomerOrder_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/{id}'], *, path_params: CustomerPortalOrdersGetPathParams) -> CustomerOrder:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/orders/{id}'], *, path_params: CustomerPortalOrdersUpdatePathParams, body: CustomerOrderUpdate) -> CustomerOrder:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/{id}/invoice'], *, path_params: CustomerPortalOrdersInvoicePathParams) -> CustomerOrderInvoice:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/orders/{id}/invoice'], *, path_params: CustomerPortalOrdersGenerateInvoicePathParams) -> Any:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/orders/{id}/payment-status'], *, path_params: CustomerPortalOrdersGetPaymentStatusPathParams) -> CustomerOrderPaymentStatus:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-portal/orders/{id}/confirm-payment'], *, path_params: CustomerPortalOrdersConfirmRetryPaymentPathParams, body: CustomerOrderConfirmPayment) -> CustomerOrderPaymentConfirmation:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/organizations/{slug}'], *, path_params: CustomerPortalOrganizationsGetPathParams) -> CustomerOrganizationData:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/subscriptions/'], *, query_params: CustomerPortalSubscriptionsListQueryParams=...) -> ListResource_CustomerSubscription_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/subscriptions/{id}'], *, path_params: CustomerPortalSubscriptionsGetPathParams) -> CustomerSubscription:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/customer-portal/subscriptions/{id}'], *, path_params: CustomerPortalSubscriptionsUpdatePathParams, body: CustomerSubscriptionUpdate) -> CustomerSubscription:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-portal/subscriptions/{id}'], *, path_params: CustomerPortalSubscriptionsCancelPathParams) -> CustomerSubscription:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/wallets/'], *, query_params: CustomerPortalWalletsListQueryParams=...) -> ListResource_CustomerWallet_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-portal/wallets/{id}'], *, path_params: CustomerPortalWalletsGetPathParams) -> CustomerWallet:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-seats'], *, query_params: CustomerSeatsListSeatsQueryParams=...) -> SeatsList:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-seats'], *, body: SeatAssign) -> CustomerSeat:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/customer-seats/{seat_id}'], *, path_params: CustomerSeatsRevokeSeatPathParams) -> CustomerSeat:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-seats/{seat_id}/resend'], *, path_params: CustomerSeatsResendInvitationPathParams) -> CustomerSeat:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-seats/claim/{invitation_token}'], *, path_params: CustomerSeatsGetClaimInfoPathParams) -> SeatClaimInfo:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-seats/claim'], *, body: SeatClaim) -> CustomerSeatClaimResponse:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/customer-sessions/'], *, body: CustomerSessionCustomerIDCreate | CustomerSessionCustomerExternalIDCreate) -> CustomerSession:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/member-sessions/'], *, body: MemberSessionCreate) -> MemberSession:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/events/'], *, query_params: EventsListQueryParams=...) -> ListResource_Event_ | ListResourceWithCursorPagination_Event_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/events/names'], *, query_params: EventsListNamesQueryParams=...) -> ListResource_EventName_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/events/{id}'], *, path_params: EventsGetPathParams) -> Event:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/events/ingest'], *, body: EventsIngest) -> EventsIngestResponse:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/event-types/'], *, query_params: EventTypesListQueryParams=...) -> ListResource_EventTypeWithStats_:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/event-types/{id}'], *, path_params: EventTypesUpdatePathParams, body: EventTypeUpdate) -> EventType:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/meters/'], *, query_params: MetersListQueryParams=...) -> ListResource_Meter_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/meters/'], *, body: MeterCreate) -> Meter:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/meters/{id}'], *, path_params: MetersGetPathParams) -> Meter:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/meters/{id}'], *, path_params: MetersUpdatePathParams, body: MeterUpdate) -> Meter:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/meters/{id}/quantities'], *, path_params: MetersQuantitiesPathParams, query_params: MetersQuantitiesQueryParams) -> MeterQuantities:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/organization-access-tokens/'], *, query_params: OrganizationAccessTokensListQueryParams=...) -> ListResource_OrganizationAccessToken_:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/v1/organization-access-tokens/'], *, body: OrganizationAccessTokenCreate) -> OrganizationAccessTokenCreateResponse:
        ...

    @overload
    async def __call__(self, method: Literal['PATCH'], path: Literal['/v1/organization-access-tokens/{id}'], *, path_params: OrganizationAccessTokensUpdatePathParams, body: OrganizationAccessTokenUpdate) -> OrganizationAccessToken:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/v1/organization-access-tokens/{id}'], *, path_params: OrganizationAccessTokensDeletePathParams) -> None:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-meters/'], *, query_params: CustomerMetersListQueryParams=...) -> ListResource_CustomerMeter_:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/customer-meters/{id}'], *, path_params: CustomerMetersGetPathParams) -> CustomerMeter:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/payments/'], *, query_params: PaymentsListQueryParams=...) -> ListResource__:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/v1/payments/{id}'], *, path_params: PaymentsGetPathParams) -> Payment:
        ...

    async def __call__(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        return await self.make_request(method, path, path_params=path_params, query_params=query_params, body=body)

    async def make_request(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        raise NotImplementedError()
