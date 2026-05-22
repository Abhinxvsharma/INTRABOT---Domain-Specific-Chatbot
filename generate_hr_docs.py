import os
from fpdf import FPDF

def create_hr_pdf(filename, title, sections):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 80, title, ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Internal HR Document - Confidental", ln=True, align='C')
    pdf.cell(0, 10, "Version 1.0 - 2026", ln=True, align='C')
    
    # Content Logic to hit ~10 pages
    for section_title, content in sections:
        pdf.add_page()
        # Section Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, section_title, ln=True)
        pdf.ln(5)
        
        # Section Content (Repeated/Detailed text to ensure length)
        pdf.set_font("Arial", '', 11)
        # We fill roughly 1.5 pages per section to reach 10 pages over 7-8 sections
        for _ in range(4): 
            pdf.multi_cell(0, 7, content)
            pdf.ln(5)
            
    # Save the file
    os.makedirs("sample_documents_to_upload", exist_ok=True)
    full_path = os.path.join("sample_documents_to_upload", filename)
    pdf.output(full_path)
    print(f"Created: {full_path}")

# Content Data
handbook_sections = [
    ("Welcome and Mission", "Welcome to IntraBot Inc. We are committed to excellence and innovation. Our mission is to provide world-class HR services using cutting-edge AI technology..."),
    ("Code of Conduct", "Employees are expected to maintain the highest standards of professional behavior. This includes punctuality, respect for colleagues, and adherence to security protocols..."),
    ("IT and Data Security", "All hardware and software provided by the company remains company property. Users must not install unauthorized software or share passwords..."),
    ("Workplace Safety", "We prioritize a safe working environment. Employees must follow all safety guidelines and report any hazards immediately to the floor manager..."),
    ("Diversity and Inclusion", "We are an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive environment for all employees..."),
    ("Performance Reviews", "Annual performance cycles help us align goals. Feedback is a two-way street, and we encourage open dialogue between managers and teams..."),
    ("Termination and Resignation", "Notice periods are defined by your specific contract. Upon leaving, all company assets must be returned in good working condition..."),
]

leave_sections = [
    ("Annual Leave Policy", "Employees are entitled to 25 days of paid annual leave per calendar year. Leave must be approved by your manager at least two weeks in advance..."),
    ("Sick Leave and Wellness", "We provide 10 days of paid sick leave. For absences longer than 3 days, a medical certificate is required from a registered practitioner..."),
    ("Parental Leave", "We offer industry-leading parental leave benefits, including 26 weeks of paid maternity leave and 4 weeks of paid paternity leave..."),
    ("Public Holidays", "The company observes all national public holidays. If a holiday falls on a weekend, the following Monday will be observed as a day off..."),
    ("Remote Work Guidelines", "Our hybrid policy allows for up to 3 days of work-from-home per week. Employees must be available during core hours (10 AM to 4 PM)..."),
    ("Bereavement Leave", "Up to 5 days of paid leave is provided in the event of the loss of an immediate family member. We support our employees during difficult times..."),
]

comp_sections = [
    ("Salary Structure", "Salaries are paid on the last working day of each month. Components include Basic Pay, HRA, Conveyance, and Special Allowance..."),
    ("Performance Bonuses", "Discretionary bonuses are awarded annually based on individual and company performance metics. These are typically paid in April..."),
    ("Health Insurance", "All employees are covered under our Group Medical Insurance policy, which includes coverage for dependents and pre-existing conditions..."),
    ("Retirement Benefits", "The company contributes 12% of basic pay towards your Provident Fund. Additional voluntary contributions are permitted..."),
    ("Stock Options (ESOPs)", "Eligible employees may receive stock options as part of their long-term incentive plan, vesting over a four-year period..."),
    ("Relocation Assistance", "For employees moving more than 50 miles, the company provides a comprehensive relocation package covering moving costs and temporary housing..."),
]

if __name__ == "__main__":
    create_hr_pdf("Employee_Handbook.pdf", "Employee Handbook", handbook_sections)
    create_hr_pdf("Leave_and_Attendance_Policy.pdf", "Leave & Attendance Policy", leave_sections)
    create_hr_pdf("Compensation_and_Benefits.pdf", "Compensation & Benefits", comp_sections)
    print("\nSuccess! Your 30 pages of HR docs are ready in 'sample_documents_to_upload/'")
