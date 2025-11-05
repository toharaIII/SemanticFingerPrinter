import random

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