from __future__ import annotations

import pandas as pd

from src.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    MOCK_LLM,
    is_llm_configured,
)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def llm_available() -> bool:
    """Return True when either mock mode or live LLM mode is available."""
    if MOCK_LLM:
        return True

    return bool(is_llm_configured() and OpenAI is not None)


def _financial_context(df: pd.DataFrame) -> str:
    """Create a safe financial summary from the logged-in user's data."""

    if df is None or df.empty:
        return "No financial transaction data is currently available."

    work = df.copy()

    work["type"] = (
        work["type"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    work["amount"] = pd.to_numeric(
        work["amount"],
        errors="coerce"
    ).fillna(0)

    income = float(
        work.loc[
            work["type"] == "income",
            "amount"
        ].sum()
    )

    expenses = float(
        work.loc[
            work["type"] == "expense",
            "amount"
        ].sum()
    )

    savings = income - expenses

    savings_rate = (
        savings / income * 100
        if income
        else 0.0
    )

    expense_rows = work[
        work["type"] == "expense"
    ]

    category = (
        expense_rows
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        if not expense_rows.empty
        else pd.Series(dtype=float)
    )

    category_text = ", ".join(
        f"{name}: ₹{amount:,.2f}"
        for name, amount in category.items()
    )

    if not category_text:
        category_text = "No category-level expense data."

    return (
    f"💵 Total income: ₹{income:,.2f}\n"
    f"💸 Total expenses: ₹{expenses:,.2f}\n"
    f"💰 Net savings: ₹{savings:,.2f}\n"
    f"📈 Savings rate: {savings_rate:.1f}%\n\n"
    f"📊 Top expense categories:\n"
    f"{category_text}\n\n"
    f"🧾 Transaction count: {len(work)}"
)

def _mock_response(
    question: str,
    transactions_df: pd.DataFrame
) -> str:
    """Local FinanceAI response used while MOCK_LLM=true."""

    context = _financial_context(transactions_df)
    text = str(question).strip().lower()

    # Financial overview
    if any(term in text for term in [
        "overview",
        "summarize",
        "summary",
        "financial situation",
        "how am i doing",
    ]):
        return (
            "📊 **Financial Overview**\n\n"
            "Here is a summary of your current financial activity:\n\n"
            f"{context}\n\n"
            "💡 **Insight**\n\n"
            "Your financial data contains both income and expense "
            "activity. Keep monitoring your largest expense categories "
            "and maintain a healthy savings rate.\n\n"
            "🧪 *Development mode: Mock LLM response.*"
        )

    # Financial advice
    if any(term in text for term in [
        "advice",
        "advise",
        "recommend",
        "recommendation",
        "what should i do",
    ]):
        return (
            "🤖 **FinanceAI Recommendation**\n\n"
            f"{context}\n\n"
            "### Suggested Actions\n\n"
            "• Monitor your highest spending categories.\n"
            "• Review recurring expenses regularly.\n"
            "• Compare actual spending with your budget.\n"
            "• Maintain an emergency savings buffer.\n\n"
            "🧪 *Development mode: Mock LLM response.*"
        )

    # General questions
    return (
        "🤖 **FinanceAI**\n\n"
        "Based on your current financial data:\n\n"
        f"{context}\n\n"
        f"**Your question:** {question}\n\n"
        "🧪 *Development mode: Mock LLM response. "
        "Live LLM generation is disabled because `MOCK_LLM=true`.*"
    )


def answer_with_llm(
    question: str,
    transactions_df: pd.DataFrame
) -> str:

    if MOCK_LLM:
        return _mock_response(
            question,
            transactions_df
        )

    if not OPENAI_API_KEY:
        raise RuntimeError(
            "LLM is not configured. "
            "Add OPENAI_API_KEY to .env."
        )

    if OpenAI is None:
        raise RuntimeError(
            "The OpenAI package is not installed."
        )

    context = _financial_context(
        transactions_df
    )

    instructions = (
        "You are FinanceAI, a personal finance assistant "
        "inside a student portfolio project. "

        "Use only the supplied financial summary as "
        "factual financial data. "

        "Do not invent transactions, balances, "
        "categories, or numbers. "

        "Explain calculations clearly when useful. "

        "Do not present yourself as a licensed "
        "financial advisor. "

        "For investment, tax, legal, credit, or other "
        "high-stakes financial decisions, provide "
        "general educational information and recommend "
        "consulting a qualified professional. "

        "If the question requires transaction-level "
        "information that is not included in the "
        "supplied summary, say that the current version "
        "cannot retrieve that detail yet."
    )

    prompt = (
        f"Financial summary:\n"
        f"{context}\n\n"
        f"User question:\n"
        f"{question}"
    )

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=instructions,
        input=prompt,
    )

    return response.output_text.strip()