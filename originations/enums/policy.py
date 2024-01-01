from enum import Enum


class PolicyRuleResultType(str, Enum):
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"
    ERRORED = "errored"


class PolicyOutcome(str, Enum):
    PASSED = "passed"
    REFERRED = "referred"
    DECLINED = "declined"
    DECLINED_WITH_REAPPLICATION_ALLOWED = "declined_with_reapplication_allowed"
    DECLINED_DUE_TO_TECHNCAL_ERROR = "declined_due_to_technical_error"
    REFERRED_DUE_TO_TECHNICAL_ERROR = "referred_due_to_technical_error"


class PolicyPhase(str, Enum):
    PREVETTING = "prevetting"
    APPLICATION = "application"
    QUOTATION = "quotation"
    SUBMISSION = "submission"


class ReferralType(str, Enum):
    PROOF_OF_INCOME = "proof_of_income"
    PROOF_OF_IDENTITY = "proof_of_identity"
    PROOF_OF_SELF = "proof_of_self"
    PROOF_OF_ADDRESS = "proof_of_address"
    PROOF_OF_BANK_ACCOUNT = "proof_of_bank_account"
    FRAUD_CHECK = "fraud_check"
