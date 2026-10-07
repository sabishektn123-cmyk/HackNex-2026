from execution.integration import (
    AgentCalculation,
    VerificationIntegration,
)


def test_agent_correct_calculation_is_verified():
    integration = VerificationIntegration()

    calculation = AgentCalculation(
        question="What is total revenue?",
        generated_code="""
revenue_a = 1000
revenue_b = 500
result = revenue_a + revenue_b
print("__VERITY_RESULT__:", result)
""",
        claimed_result=1500,
        dataset="sales.csv",
    )

    result = integration.verify_agent_calculation(calculation)

    assert result.status == "VERIFIED"
    assert result.actual == 1500.0


def test_agent_wrong_claim_fails_verification():
    integration = VerificationIntegration()

    calculation = AgentCalculation(
        question="What is total revenue?",
        generated_code="""
revenue_a = 1000
revenue_b = 500
result = revenue_a + revenue_b
print("__VERITY_RESULT__:", result)
""",
        claimed_result=2000,
        dataset="sales.csv",
    )

    result = integration.verify_agent_calculation(calculation)

    assert result.status == "VERIFICATION_FAILED"
    assert result.expected == 2000.0
    assert result.actual == 1500.0


def test_agent_unsafe_code_cannot_be_verified():
    integration = VerificationIntegration()

    calculation = AgentCalculation(
        question="What is the result?",
        generated_code="""
import os
os.system("whoami")
print("__VERITY_RESULT__:", 1)
""",
        claimed_result=1,
        dataset="data.csv",
    )

    result = integration.verify_agent_calculation(calculation)

    assert result.status == "CANNOT_DETERMINE"
    assert result.status != "VERIFIED"


def test_agent_missing_result_abstains():
    integration = VerificationIntegration()

    calculation = AgentCalculation(
        question="What is total?",
        generated_code="""
values = [100, 200]
total = sum(values)
print(total)
""",
        claimed_result=300,
        dataset="data.csv",
    )

    result = integration.verify_agent_calculation(calculation)

    assert result.status == "CANNOT_DETERMINE"


def test_agent_ambiguous_calculation_abstains():
    integration = VerificationIntegration()

    calculation = AgentCalculation(
        question="What is the answer?",
        generated_code="""
result = 500
print("__VERITY_RESULT__:", result)
""",
        claimed_result=500,
        dataset="data.csv",
    )

    result = integration.verify_agent_calculation(
        calculation,
        ambiguous=True,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_agent_conflicting_data_abstains():
    integration = VerificationIntegration()

    calculation = AgentCalculation(
        question="What is the answer?",
        generated_code="""
result = 500
print("__VERITY_RESULT__:", result)
""",
        claimed_result=500,
        dataset="data.csv",
    )

    result = integration.verify_agent_calculation(
        calculation,
        conflicting=True,
    )

    assert result.status == "CANNOT_DETERMINE"