import random

import random

def generate_mock_tax_analysis():
    """
    Generates a pseudo-random mock response for a tax analysis agent.
    Returns a structured 3-paragraph response with Summary, Key Payments, and Additional Information.
    Maintains consistent factual data while varying presentation and word choice.
    """
    
    # Fixed factual data (consistent across all responses)
    TAX_YEAR = "2024"
    ENTITY_TYPE = "individual taxpayer"
    FILING_STATUS = "married filing jointly"
    INCOME_RANGE = "$142,000"
    TAX_BRACKET = "22%"
    PAYMENT_AMOUNT = "$12,450"
    PAYMENT_DATE = "April 15th"
    PENALTY_AMOUNT = "$485"
    CREDIT_TYPE = "Child Tax Credit"
    DEDUCTION_TYPE = "mortgage interest deduction"
    
    # Varying presentation styles for the same information
    summary_intros = [
        "The tax analysis for",
        "Based on the review of",
        "After analyzing",
        "The assessment for"
    ]
    
    summary_indicators = [
        "indicates that",
        "shows that",
        "reveals that",
        "demonstrates that"
    ]
    
    summary_bracket_phrases = [
        f"falls within the {TAX_BRACKET} federal tax bracket",
        f"is subject to the {TAX_BRACKET} marginal tax rate",
        f"places them in the {TAX_BRACKET} federal bracket",
        f"qualifies for the {TAX_BRACKET} tax bracket"
    ]
    
    summary_closings = [
        "All calculations comply with current IRS regulations and take into account applicable deductions and credits.",
        "The assessment follows current IRS guidelines and incorporates relevant deductions and available credits.",
        "This analysis adheres to IRS standards and includes all applicable deductions and credit considerations.",
        "The calculation aligns with IRS requirements and reflects appropriate deductions and credits."
    ]
    
    payment_intros = [
        f"A payment of {PAYMENT_AMOUNT} is due by {PAYMENT_DATE}.",
        f"The required payment of {PAYMENT_AMOUNT} must be submitted by {PAYMENT_DATE}.",
        f"A total of {PAYMENT_AMOUNT} is owed, with a deadline of {PAYMENT_DATE}.",
        f"Payment in the amount of {PAYMENT_AMOUNT} should be remitted by {PAYMENT_DATE}."
    ]
    
    payment_penalty_phrases = [
        f"Failure to remit payment by this date may result in a late filing penalty of approximately {PENALTY_AMOUNT}.",
        f"Missing this deadline could incur a penalty of around {PENALTY_AMOUNT}.",
        f"Late payment may trigger penalties totaling approximately {PENALTY_AMOUNT}.",
        f"Non-compliance with this deadline may lead to a {PENALTY_AMOUNT} penalty."
    ]
    
    payment_credit_phrases = [
        f"Additionally, the taxpayer may be eligible for the {CREDIT_TYPE}, which could reduce the overall tax burden.",
        f"The taxpayer qualifies for the {CREDIT_TYPE}, potentially lowering the total liability.",
        f"Eligibility for the {CREDIT_TYPE} has been confirmed, which may decrease the final amount owed.",
        f"The {CREDIT_TYPE} is applicable in this case and may reduce the net tax obligation."
    ]
    
    payment_deduction_phrases = [
        f"The {DEDUCTION_TYPE} has been factored into the final calculation.",
        f"The calculation includes the {DEDUCTION_TYPE}.",
        f"The {DEDUCTION_TYPE} is reflected in the total assessment.",
        f"The final amount accounts for the {DEDUCTION_TYPE}."
    ]
    
    additional_recommendations = [
        "Consider consulting with a tax professional for detailed planning.",
        "It may be beneficial to work with a qualified tax advisor for comprehensive planning.",
        "Professional tax consultation is recommended for optimal planning strategies.",
        "Engaging a tax professional could provide valuable planning insights."
    ]
    
    additional_next_steps = [
        "it is advised to review quarterly estimated payments to avoid underpayment penalties",
        "reviewing estimated quarterly payments is recommended to prevent underpayment issues",
        "ensure quarterly estimated payments are assessed to avoid potential penalties",
        "quarterly payment estimates should be examined to maintain compliance"
    ]
    
    additional_closings = [
        "Documentation should be retained for a minimum of three years in accordance with IRS guidelines. Any discrepancies or questions regarding this analysis should be addressed promptly to ensure compliance and optimize tax positioning.",
        "All supporting documentation must be kept for at least three years per IRS requirements. Questions or concerns about this assessment should be resolved quickly to maintain compliance and maximize tax efficiency.",
        "Records should be maintained for no less than three years as required by the IRS. Any uncertainties or issues with this analysis warrant immediate attention to ensure proper compliance and tax optimization.",
        "The IRS requires documentation retention for a minimum three-year period. Promptly address any questions or discrepancies related to this analysis to preserve compliance and enhance tax outcomes."
    ]
    
    # Generate the structured response with varied presentation
    summary = (
        f"Summary\n\n"
        f"{random.choice(summary_intros)} {TAX_YEAR} {random.choice(summary_indicators)} the {ENTITY_TYPE} "
        f"with {FILING_STATUS} status and income of {INCOME_RANGE} "
        f"{random.choice(summary_bracket_phrases)}. Based on the claimed deductions, "
        f"the calculated tax liability has been assessed. "
        f"{random.choice(summary_closings)}"
    )
    
    key_payments = (
        f"Key Payments\n\n"
        f"{random.choice(payment_intros)} "
        f"{random.choice(payment_penalty_phrases)} "
        f"{random.choice(payment_credit_phrases)} "
        f"{random.choice(payment_deduction_phrases)}"
    )
    
    additional_info = (
        f"Additional Information\n\n"
        f"{random.choice(additional_recommendations)} For the upcoming tax period, "
        f"{random.choice(additional_next_steps)}. "
        f"{random.choice(additional_closings)}"
    )
    
    return f"{summary}\n\n{key_payments}\n\n{additional_info}"





def call_orchestrator(prompt: str, plan: str = None, document=None) -> str:
    """
    Mocked call to orchestrator that simulates realistic LLM variance
    for W-2 financial document analysis. In production, replace this
    with an HTTP POST to Rocket Mortgage's AI orchestrator endpoint.
    """
    
    # Base W-2 data (consistent across outputs)
    gross_wages = 78500
    federal_tax = 14230
    state_tax = 3925
    ss_wages = 78500
    ss_tax = 4867
    medicare_wages = 78500
    medicare_tax = 1138.25
    
    # Variance dimensions
    intro_styles = [
        "Based on the provided W-2 form, here is a comprehensive analysis:",
        "I've analyzed the W-2 tax form and identified the following key information:",
        "Here's a structured breakdown of your W-2 form:",
        "After reviewing your W-2, here are the important details:",
        "W-2 Analysis Summary:",
        "Analysis of W-2 Tax Form:",
    ]
    
    structure_types = ["headers", "bullets", "numbered", "prose"]
    detail_levels = ["concise", "moderate", "verbose"]
    
    # Randomly select style components
    intro = random.choice(intro_styles)
    structure = random.choice(structure_types)
    detail = random.choice(detail_levels)
    include_summary = random.choice([True, False])
    
    # Build output based on selected style
    output = intro + "\n\n"
    
    if structure == "headers":
        output += "**Annual Compensation:**\n"
        output += f"Your gross wages for the year totaled ${gross_wages:,}.\n\n"
        
        output += "**Federal Tax Withholding:**\n"
        if detail == "verbose":
            output += f"A total of ${federal_tax:,} was withheld for federal income tax throughout the year, representing approximately {(federal_tax/gross_wages)*100:.1f}% of your gross income.\n\n"
        else:
            output += f"Federal tax withheld: ${federal_tax:,}\n\n"
        
        output += "**State Tax Withholding:**\n"
        output += f"State tax withheld: ${state_tax:,}\n\n"
        
        output += "**Social Security Contributions:**\n"
        if detail == "verbose":
            output += f"Social Security wages: ${ss_wages:,}\nSocial Security tax withheld: ${ss_tax:,.2f} (6.2% of SS wages)\n\n"
        else:
            output += f"SS wages: ${ss_wages:,} | SS tax: ${ss_tax:,.2f}\n\n"
        
        output += "**Medicare Contributions:**\n"
        output += f"Medicare wages: ${medicare_wages:,} | Medicare tax: ${medicare_tax:,.2f}\n\n"
    
    elif structure == "bullets":
        output += f"• Gross Wages: ${gross_wages:,}\n"
        output += f"• Federal Tax Withheld: ${federal_tax:,}\n"
        output += f"• State Tax Withheld: ${state_tax:,}\n"
        
        if detail == "verbose":
            output += f"• Social Security: ${ss_tax:,.2f} withheld from ${ss_wages:,} in SS wages (6.2% rate)\n"
            output += f"• Medicare: ${medicare_tax:,.2f} withheld from ${medicare_wages:,} in Medicare wages (1.45% rate)\n\n"
        else:
            output += f"• Social Security Tax: ${ss_tax:,.2f}\n"
            output += f"• Medicare Tax: ${medicare_tax:,.2f}\n\n"
    
    elif structure == "numbered":
        output += f"1. Gross Wages: ${gross_wages:,}\n"
        output += f"2. Federal Income Tax: ${federal_tax:,} withheld\n"
        output += f"3. State Income Tax: ${state_tax:,} withheld\n"
        output += f"4. Social Security: ${ss_tax:,.2f} (from ${ss_wages:,} in wages)\n"
        output += f"5. Medicare: ${medicare_tax:,.2f} (from ${medicare_wages:,} in wages)\n\n"
    
    else:  # prose
        if detail == "concise":
            output += f"Your W-2 shows gross wages of ${gross_wages:,}. Federal tax withholding was ${federal_tax:,} and state tax withholding was ${state_tax:,}. "
            output += f"Social Security contributions totaled ${ss_tax:,.2f} and Medicare contributions were ${medicare_tax:,.2f}.\n\n"
        elif detail == "moderate":
            output += f"The W-2 form indicates that you earned ${gross_wages:,} in gross wages during the tax year. "
            output += f"Your employer withheld ${federal_tax:,} for federal income tax and ${state_tax:,} for state income tax. "
            output += f"Additionally, ${ss_tax:,.2f} was withheld for Social Security and ${medicare_tax:,.2f} for Medicare.\n\n"
        else:  # verbose
            output += f"According to your W-2 tax form, your total gross wages for the year amounted to ${gross_wages:,}. "
            output += f"Throughout the year, your employer withheld ${federal_tax:,} for federal income tax purposes, which represents approximately {(federal_tax/gross_wages)*100:.1f}% of your gross income. "
            output += f"State income tax withholding totaled ${state_tax:,}. "
            output += f"For Social Security, ${ss_tax:,.2f} was withheld based on your Social Security wages of ${ss_wages:,}, "
            output += f"while Medicare contributions amounted to ${medicare_tax:,.2f} based on Medicare wages of ${medicare_wages:,}.\n\n"
    
    # Optional summary section (adds more variance)
    if include_summary:
        total_tax = federal_tax + state_tax + ss_tax + medicare_tax
        effective_rate = (total_tax / gross_wages) * 100
        
        summary_intros = [
            "In summary,",
            "Overall,",
            "To summarize,",
            "Key takeaway:",
        ]
        
        summary_styles = [
            f"{random.choice(summary_intros)} your total tax obligations (federal, state, SS, and Medicare) came to ${total_tax:,.2f}, representing an effective rate of {effective_rate:.1f}%.",
            f"{random.choice(summary_intros)} total withholdings across all categories amounted to ${total_tax:,.2f}.",
            f"Your net take-home after all withholdings would be approximately ${gross_wages - total_tax:,.2f}.",
        ]
        
        output += random.choice(summary_styles)
    
    return output.strip()
