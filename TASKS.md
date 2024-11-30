# Tasks

## Preface

This document outlines a series of workflows designed to automate dental administrative tasks using LangGraph. The workflows progress from simple to more complex, providing a structured approach to building functionality while adhering to LangGraph best practices. Each workflow is designed to be a cohesive process that can be implemented using LangGraph's stateful, graph-based orchestration capabilities.

---

### **Phase 0: Setup**

**Task 1: Basic Google Search**

- **Objective:** Test basic functionality of a langgraph agent being able to use the Agent-D API
- **Details:**
  - Navigate to google.com
  - Use the google search tool to search for the latest weather in Kansas City

### **Phase 1: Basic Navigation and Authentication**

**Task 1: MoHealthNet Portal (eMOMED) Login**

- **Objective:** Log into the MoHealthNet provider portal (emomed.com)
- **Details:**
  - Navigate to emomed.com
  - Use the enter secrets tool to log in
  - If login fails, terminate and report the error message
  - Verify successful login by matching URL to: emomed.com/portal/wps/myportal

**Task 2: Envolve Dental Login**

- **Objective:** Log into the Envolve Dental provider portal
- **Details:**
  - Navigate to pwp.envolvedental.com
  - Use the enter secrets tool to log in
  - If login fails, terminate and report the error message
  - Verify successful login by matching URL to: pwp.envolvedental.com/PWP/Dental

**Task 3: DentaQuest Login**

- **Objective:** Log into the DentaQuest provider portal with MFA handling
- **Details:**
  - Navigate to providers.dentaquest.com
  - Use the enter secrets tool to log in
  - Handle email verification code if prompted
  - If login fails, terminate and report the error message
  - Verify successful login by matching URL to: providers.dentaquest.com/dashboard/

**Task 4: UnitedHealthcare Dental Login**

- **Objective:** Log into the UnitedHealthcare Dental portal (DentalHub)
- **Details:**
  - Navigate to app.dentalhub.com
  - If redirected to login page, click the login button
  - Use the enter secrets tool to log in
  - If login fails, terminate and report the error message
  - Verify successful login by matching URL to: app.dentalhub.com/app/dashboard

**Task 5: CyberAccess Login**

- **Objective:** Log into CyberAccess with license agreement handling
- **Details:**
  - Navigate to cyberaccessonline.net
  - Use the enter secrets tool to log in
  - When prompted, read and click "I Agree" on the license agreement
  - Wait for the final loading screen to complete
  - If login fails, terminate and report the error message
  - Verify successful login by matching URL to: cyberaccessonline.net/CyberAccess/ProviderPortal.aspx

**Task 6: Curve Dental Login**

- **Objective:** Log into Curve Dental for Comfort Dental South Independence
- **Details:**
  - Navigate to comfortdentalsid.curvehero.com/#/
  - Check for redirect to login page
  - Use the enter secrets tool to log in
  - If login fails, terminate and report the error message
  - Verify successful login by matching URL to: comfortdentalsid.curvehero.com/#/

---

### **Phase 2: Basic Navigation and Data Retrieval**

**Task 4: Navigate to Eligibility Verification in MoHealthNet**

- **Objective:** After logging in, navigate to the "Eligibility Verification" section.  
- **Details:**  
  - From the dashboard, identify and click on the "Eligibility Verification" tab.  
  - Handle any dropdown menus or sub-sections.  
  - Prepare to input patient information for verification.

**Task 5: Verify Medicaid Eligibility and Primary Insurance for John Doe**

- **Objective:** Verify Medicaid eligibility for John Doe (DOB: May 5, 2010), retrieving his DCN, list of benefits/coverage, and checking for any primary insurance information (e.g., primary PPO or Medicare).  
- **Details:**  
  - In the "Eligibility Verification" section, enter John Doe's details.  
  - Retrieve and record his DCN number.  
  - Extract detailed benefits and coverage information.  
  - Check for indications of primary insurance coverage.  
    - If primary insurance is detected, flag for human verification.  
    - Note that submitting Medicaid as secondary requires EOB from primary insurer.

**Task 6: Retrieve Medication History and Diagnosis Codes from CyberAccess**

- **Objective:** Retrieve medication history and diagnosis codes for Jane Smith (DOB: August 15, 2005).  
- **Details:**  
  - Search for Jane Smith using her DOB and other identifiers.  
  - Access her medication history records.  
  - Extract any diagnosis codes available.  
  - Compile the information into a structured format for review.

**Task 7: Retrieve Additional Patient Data from CyberAccess**

- **Objective:** For a selected patient, retrieve pharmacy information and any other relevant data.  
- **Details:**  
  - Select a patient, e.g., Michael Brown (DOB: March 22, 2008).  
  - Access pharmacy information, including preferred pharmacy.  
  - Extract other pertinent medical data such as allergies or treatment history.  
  - Present the consolidated data coherently.

---

### **Phase 3: Data Entry and Integration**

**Task 8: Extract Intake Data from JotForm and Enter into Curve Dental**

- **Objective:** Extract intake data for Olivia Wilson from JotForm and enter her demographic and insurance information into Curve Dental.  
- **Details:**  
  - Access Olivia Wilson's completed JotForm submission.  
  - Extract demographic details: name, address, contact information.  
  - Retrieve insurance information provided.  
  - Log into Curve Dental and create a new patient profile.  
  - Input all extracted data accurately into the system.

**Task 9: Consolidate Demographic Information from Multiple Sources**

- **Objective:** Retrieve demographic and insurance info from MoHealthNet and CyberAccess for Liam Johnson (DOB: July 12, 2009\) and enter it into the practice management system.  
- **Details:**  
  - Search for Liam Johnson in both MoHealthNet and CyberAccess.  
  - Compare and consolidate demographic data from both sources.  
  - Identify any discrepancies and flag them for review.  
  - Enter the unified data into Curve Dental, ensuring consistency.

---

### **Phase 4: Claims Preparation and Submission**

**Task 10: Prepare an ADA 2024 Claim Form in the PMS**

- **Objective:** After entering patient data into the PMS, prepare an ADA 2024 claim form for services provided to Ethan Taylor (DOB: November 5, 2007).  
- **Details:**  
  - Input the services rendered, e.g., procedure codes D0120 (periodic oral evaluation) and D1120 (prophylaxis-child).  
  - Ensure all patient and provider information is correctly filled out.  
  - Validate that the claim form is complete and accurate before submission.

**Task 11: Analyze and Adjust Claim for Medicaid Compliance**

- **Objective:** Ensure the claim is compliant with Medicaid requirements, adjusting procedure codes if necessary.  
- **Details:**  
  - Review the claim for non-covered codes.  
  - Replace any non-covered codes with Medicaid-approved alternatives.  
    - For example, replace D0210 (intraoral \- complete series) with appropriate individual periapical codes.  
  - Document any adjustments made for auditing purposes.  
  - If prior authorization is required, proceed to initiate it.

**Task 12: Initiate Prior Authorization if Needed**

- **Objective:** Identify procedures requiring prior authorization and initiate the process.  
- **Details:**  
  - Determine if any services need prior authorization based on Medicaid guidelines.  
  - Access the prior authorization forms on the relevant portal.  
  - Fill out the necessary information, including procedure details and justification.  
  - Submit the prior authorization request electronically.  
  - Record confirmation of submission and any reference numbers.

**Task 13: Submit a New Claim via Envolve Dental Provider Portal**

- **Objective:** Log into Envolve Dental and submit a new claim for Lucas Miller (DOB: September 9, 2012), including procedure codes D1120 and D1208.  
- **Details:**  
  - Access the claims submission section in Envolve Dental.  
  - Enter patient details and verify eligibility.  
  - Input procedure codes and verify they are covered.  
  - Attach any necessary documentation.  
  - Submit the claim and record the submission confirmation.

**Task 14: Check Claim Status and Address Denials**

- **Objective:** Check the status of Lucas Miller's submitted claim and report if it's approved, denied, or pending.  
- **Details:**  
  - Access the claim tracking section.  
  - Locate Lucas Miller's claim using reference numbers or patient details.  
  - Record the current status.  
  - If denied or pending, retrieve the reason for denial.  
  - Suggest corrective actions or flag for human intervention.

---

### **Phase 5: Claims Tracking and EOB Management**

**Task 15: Monitor Claims and Prepare for EOB Retrieval**

- **Objective:** Track the status of submitted claims over time, noting changes and preparing to handle Explanation of Benefits (EOBs) when available.  
- **Details:**  
  - Set up automated tracking for multiple claims.  
  - Receive notifications for status updates.  
  - Maintain a log of all claim statuses and changes.  
  - Anticipate EOB availability based on claim processing timelines.

**Task 16: Download EOB for Noah Anderson from UnitedHealthcare Dental**

- **Objective:** Once the claim reaches the EOB stage, download the EOB document.  
- **Details:**  
  - Log into UnitedHealthcare Dental provider portal.  
  - Navigate to the EOB retrieval section.  
  - Locate Noah Anderson's (DOB: December 18, 2010\) EOB.  
  - Download the EOB securely.  
  - Store it according to HIPAA-compliant data management practices.

---

### **Phase 6: Advanced Data Consolidation and Error Handling**

**Task 17: Consolidate Comprehensive Patient Data into a Summary Document**

- **Objective:** For Sophia Martinez (DOB: June 1, 2011), consolidate her medical history, medications, diagnosis codes, pharmacy information, and insurance eligibility from multiple sources into a single summary document.  
- **Details:**  
  - Extract data from MoHealthNet, CyberAccess, and DentaQuest.  
  - Organize the data into categories (e.g., medical history, medications).  
  - Identify and highlight any critical health information.  
  - Format the summary document professionally for clinical use.

**Task 18: Resolve Data Discrepancies Across Sources**

- **Objective:** Detect and resolve discrepancies in patient data from multiple sources.  
- **Details:**  
  - Compare data points such as DOB, names, and policy numbers.  
  - Highlight inconsistencies for review.  
  - Cross-reference with additional sources if available.  
  - Flag significant discrepancies that may affect care or billing.

**Task 19: Implement Robust Error Handling and Retry Mechanisms**

- **Objective:** Detect failed operations, handle errors gracefully, and retry or escalate as needed.  
- **Details:**  
  - Simulate a failed login due to incorrect credentials on DentaQuest.  
  - Detect the error message and log it.  
  - Retry the login with the correct credentials.  
  - If the issue persists, notify an administrator with detailed error information.

---

### **Phase 7: Agent Adaptability and Compliance**

**Task 20: Adapt to Portal Layout Changes on High-Priority Portals**

- **Objective:** Adjust navigation strategies to accommodate layout changes on portals like Envolve Dental or UnitedHealthcare Dental.  
- **Details:**  
  - Detect changes in DOM structure or element locations.  
  - Utilize flexible selectors or machine learning models to find necessary elements.  
  - Continue operations without manual intervention.  
  - Log changes and adaptations made for future reference.

**Task 21: Maintain Active Sessions and Automate Re-Authentication**

- **Objective:** Manage sessions across multiple portals, ensuring continuous operation.  
- **Details:**  
  - Keep track of session timeouts for each portal.  
  - Automate re-authentication processes when sessions expire.  
  - Ensure no data is lost or processes interrupted during re-authentication.  
  - Securely handle credentials during automatic logins.

**Task 22: Ensure Compliance with HIPAA Regulations**

- **Objective:** Handle all patient data securely, adhering to HIPAA regulations.  
- **Details:**  
  - Encrypt data at rest and in transit.  
  - Implement strict access controls and authentication measures.  
  - Maintain audit logs of data access and actions taken.  
  - Regularly update security protocols and conduct compliance audits.

**Task 23: Generate Detailed Audit Trails**

- **Objective:** Document all agent actions for compliance verification.  
- **Details:**  
  - Log timestamps, actions performed, and data accessed.  
  - Record any adjustments made to claims or patient data.  
  - Store logs in a secure, tamper-evident system.  
  - Provide audit trails upon request for compliance checks.

---

### **Phase 8: Workflow Automation and Optimization**

**Task 24: Automate End-to-End Claims Processing for Isabella Thomas**

- **Objective:** Automate the full workflow, including eligibility verification, data extraction, prior authorization, code adjustments, claim submission, and status tracking.  
- **Details:**  
  - Begin with patient data retrieval from multiple sources.  
  - Verify eligibility and identify any primary insurance.  
  - Prepare and adjust the claim as per Medicaid guidelines.  
  - Initiate prior authorizations if needed.  
  - Submit the claim and set up status monitoring.  
  - Handle any exceptions or errors throughout the process.

**Task 25: Optimize Performance for Processing Multiple Patients**

- **Objective:** Enhance agent performance to efficiently process data for 100 patients.  
- **Details:**  
  - Implement parallel processing where appropriate.  
  - Manage system resources to prevent overutilization.  
  - Monitor performance metrics and adjust strategies.  
  - Ensure that processing large volumes does not compromise accuracy.

**Task 26: Adapt Agent Behaviors Using Historical Data**

- **Objective:** Use past interactions to improve efficiency and error handling.  
- **Details:**  
  - Analyze historical data for patterns in portal responsiveness.  
  - Adjust timeouts and retries based on previous successes and failures.  
  - Implement predictive navigation paths to speed up processes.  
  - Continuously learn from new data to refine operations.

**Task 27: Develop a Comprehensive Monitoring Dashboard**

- **Objective:** Provide a user interface for monitoring agent activities and managing operations.  
- **Details:**  
  - Display real-time statuses of tasks and processes.  
  - Include error logs with detailed information.  
  - Offer controls to start, stop, or modify agent operations.  
  - Centralize actionable tasks requiring human intervention (e.g., primary insurance verification).  
  - Ensure the dashboard is secure and accessible only to authorized personnel.

**Task 28: Facilitate Human-in-the-Loop for Critical Decisions**

- **Objective:** Identify tasks requiring human input and integrate prompts into workflows.  
- **Details:**  
  - Detect when a patient has primary insurance other than Medicaid.  
  - Prompt human operators to verify primary insurance details.  
  - Provide necessary information and interface for humans to input decisions.  
  - Resume automated processes upon receiving human input.

**Task 29: Handle Secondary Medicaid Claims Appropriately**

- **Objective:** Ensure that claims for patients with Medicaid as secondary insurance are processed correctly.  
- **Details:**  
  - Identify patients with primary PPO or Medicare insurance.  
  - Avoid entering secondary Medicaid credentials into the PMS without primary EOBs.  
  - Flag these cases for human follow-up.  
  - Provide guidance on obtaining and inputting primary EOBs to proceed with the claim.

---

### **Phase 9: Deployment and Environment Management**

**Task 30: Deploy Agent in Test and Production Environments**

- **Objective:** Ensure the agents operates consistently across environments.  
- **Details:**  
  - Set up separate configurations for test and production.  
  - Validate that all functionalities work as expected in both.  
  - Implement environment-specific variables securely.

**Task 31: Conduct User Acceptance Testing (UAT) with Staff**

- **Objective:** Gather feedback from actual users to refine the agent.  
- **Details:**  
  - Allow staff to interact with the agent and perform real-world tasks.  
  - Collect feedback on usability, efficiency, and accuracy.  
  - Identify any issues or areas for improvement.  
  - Iterate on the agent's design based on user insights.

**Task 32: Provide Training and Documentation for Users**

- **Objective:** Equip users with the knowledge to effectively use and manage the agent.  
- **Details:**  
  - Develop comprehensive user manuals and quick-start guides.  
  - Create troubleshooting resources for common issues.  
  - Conduct training sessions or webinars as needed.  
  - Ensure documentation is kept up-to-date with system changes.

---

### **Additional Considerations**

- **Prior Authorizations (PAs):** Include tasks for sending out PAs, tracking their status, and ensuring they are attached to claims when required.  
- **Tracking Secondary Medicaid Payments:** Implement processes for sending primary EOBs when processing secondary Medicaid payments to prevent claim denials.  
- **Portal Prioritization:** Focus adaptability and change detection efforts on portals that are prone to updates, such as Envolve Dental and UnitedHealthcare Dental.  
- **Security Emphasis:** Throughout all tasks, maintain a strong focus on data protection, encryption, and compliance with all relevant regulations.
