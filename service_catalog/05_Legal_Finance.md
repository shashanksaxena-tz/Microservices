# Legal, Finance & Business Services (201-250)

This catalog details AI-native microservices focused on Legal Tech, Fintech, and Business Operations.

## 201. Contract Clause Extractor
* **Description**: Automatically identifies and extracts specific clauses (Indemnity, Termination, Liability) from long legal contracts.
* **Features**:
  * Classification of 50+ clause types.
  * Deviation detection (standard vs. non-standard).
* **Requirements**:
  * **Models**: LegalBERT.
* **UI Flow**:
  1. Upload PDF Contract.
  2. Sidebar list: "Termination Clause (Page 5)".
  3. Click to jump and highlight.

## 202. Legal Risk Scorer
* **Description**: Analyzes a contract or document to assign a risk score based on unfavorable terms.
* **Features**:
  * Red/Yellow/Green risk indicators.
  * Explanation of risk factors.
* **Requirements**:
  * **Models**: Finetuned Transformer on legal judgments.
* **UI Flow**:
  1. Dashboard view of uploaded contracts.
  2. "Risk Score: High (85/100)".
  3. "Why? Unlimited liability clause detected."

## 203. Case Law Finder
* **Description**: Finds relevant legal precedents and case law based on a natural language description of a situation.
* **Features**:
  * Jurisdiction filtering.
  * Semantic search (not just keyword).
* **Requirements**:
  * **Data**: Caselaw Access Project API.
* **UI Flow**:
  1. Query: "Tenant rights regarding mold in Florida".
  2. List of cases: "Smith v. Landlord (2015)..."

## 204. NDA Generator
* **Description**: Generates a customized Non-Disclosure Agreement based on user inputs.
* **Features**:
  * One-way vs Mutual.
  * Jurisdiction selection.
* **Requirements**:
  * **Models**: Template-based generation.
* **UI Flow**:
  1. Form: "Who are parties?", "State?".
  2. "Generate PDF".

## 205. Invoice Parser
* **Description**: Extracts structured data (Vendor, Date, Line Items, Total) from invoice images or PDFs.
* **Features**:
  * Table extraction.
  * Currency normalization.
* **Requirements**:
  * **Models**: LayoutLM, Donut.
* **UI Flow**:
  1. Email forward or Upload.
  2. JSON Output: `{"total": 500.00, "vendor": "AWS"}`.

## 206. Receipt Scanner
* **Description**: Scans receipts for expense reporting.
* **Features**:
  * Mobile-friendly.
  * Handwriting support (tips).
* **Requirements**:
  * **Models**: OCR.
* **UI Flow**:
  1. Photo of crumpled receipt.
  2. Auto-fill expense report form.

## 207. Expense Categorizer
* **Description**: Categorizes bank transactions into accounting codes (Travel, Meals, SaaS).
* **Features**:
  * MCC code analysis.
  * Merchant name normalization.
* **Requirements**:
  * **Models**: Classification (XGBoost/BERT).
* **UI Flow**:
  1. Bank feed stream.
  2. "Uber" -> "Travel".

## 208. Financial News Sentiment Analyzer
* **Description**: Monitors news feeds for sentiment affecting specific tickers or markets.
* **Features**:
  * Impact scoring.
  * Real-time alerts.
* **Requirements**:
  * **Models**: FinBERT.
* **UI Flow**:
  1. Dashboard for "AAPL".
  2. Gauge: "Bullish (News: Record Earnings)".

## 209. Stock Prediction Signal
* **Description**: Generates buy/sell signals based on multi-modal data (price, news, social).
* **Features**:
  * Technical + Fundamental analysis.
  * Confidence intervals.
* **Requirements**:
  * **Models**: LSTM / Temporal Fusion Transformer.
* **UI Flow**:
  1. Chart with "Buy" arrow overlay.
  2. "Confidence: 60%".

## 210. Fraud Pattern Detector
* **Description**: Detects complex fraud patterns in transaction data.
* **Features**:
  * Graph-based detection (money mule rings).
  * Velocity checks.
* **Requirements**:
  * **Models**: Graph Neural Networks.
* **UI Flow**:
  1. Admin alert: "Suspicious ring detected".
  2. Visual graph of connected accounts.

## 211. Credit Risk Assessor
* **Description**: Estimates creditworthiness using alternative data (rent, utility payments) for thin-file borrowers.
* **Features**:
  * Cashflow underwriting.
  * Explainable AI (rejection reasons).
* **Requirements**:
  * **Models**: Gradient Boosting.
* **UI Flow**:
  1. Connect Bank Account.
  2. "Approved. Limit: $5,000".

## 212. Transaction Anomaly Detector
* **Description**: Flags unusual transactions for a specific user profile (e.g., large purchase in foreign country).
* **Features**:
  * User behavior profiling.
  * Geo-location checks.
* **Requirements**:
  * **Models**: Isolation Forest.
* **UI Flow**:
  1. Push notification: "Did you spend $500 in Lagos?"
  2. Yes/No buttons.

## 213. Regulatory Compliance Checker
* **Description**: Checks marketing text or financial advice against regulations (SEC, FTC).
* **Features**:
  * Disclaimers verification.
  * "Guaranteed returns" detection.
* **Requirements**:
  * **Models**: Rule-based + NLP.
* **UI Flow**:
  1. Paste ad copy.
  2. Warning: "Missing 'Past performance' disclaimer."

## 214. Tax Document Analyzer
* **Description**: Extracts relevant tax information from W-2s, 1099s, etc.
* **Features**:
  * Multi-form support.
  * Cross-checking.
* **Requirements**:
  * **Models**: Document AI.
* **UI Flow**:
  1. Upload pile of PDFs.
  2. Summary table of Income/Withholding.

## 215. Portfolio Optimizer Suggestion
* **Description**: Suggests portfolio rebalancing to maximize Sharpe ratio or meet goals.
* **Features**:
  * Risk tolerance alignment.
  * Tax-loss harvesting opportunities.
* **Requirements**:
  * **Models**: Modern Portfolio Theory algos.
* **UI Flow**:
  1. "Current Allocation vs Target".
  2. "Sell 5% SPY, Buy 5% BND".

## 216. Loan Application Reviewer
* **Description**: Automates the initial screening of loan applications.
* **Features**:
  * Document completeness check.
  * DTI (Debt-to-Income) calc.
* **Requirements**:
  * **Models**: OCR + Logic.
* **UI Flow**:
  1. Loan Officer Dashboard.
  2. "Application #123: Ready for review (All docs present)".

## 217. Insurance Claim Analyzer
* **Description**: Validates insurance claims against policy coverage and evidence.
* **Features**:
  * Photo damage assessment (Vision).
  * Policy limit check.
* **Requirements**:
  * **Models**: Multi-modal.
* **UI Flow**:
  1. Claim details view.
  2. "Recommendation: Approve. Est value: $500".

## 218. Market Trend Forecaster
* **Description**: Predicts macro trends based on search volume and social chatter.
* **Features**:
  * "Rising topics".
  * Sector rotation signals.
* **Requirements**:
  * **Data**: Google Trends / Twitter.
* **UI Flow**:
  1. Report: "Electric Bikes trending up 50%".

## 219. Competitor Analysis Agent
* **Description**: Monitors competitor websites and news for changes in pricing or messaging.
* **Features**:
  * Change detection.
  * Strategy inference.
* **Requirements**:
  * **Tools**: Web Scraper.
* **UI Flow**:
  1. Weekly email.
  2. "Competitor X lowered pricing by 10%".

## 220. Annual Report Summarizer
* **Description**: Summarizes 10-K and 10-Q reports, extracting key risks and financial metrics.
* **Features**:
  * Year-over-year comparison.
  * "Management Discussion" sentiment.
* **Requirements**:
  * **Models**: Long-context LLM.
* **UI Flow**:
  1. Upload 100-page PDF.
  2. 2-page Exec Summary.

## 221. Job Description Generator
* **Description**: Creates inclusive and optimized JDs from a list of requirements.
* **Features**:
  * Bias removal.
  * SEO optimization.
* **Requirements**:
  * **Models**: Generative Text.
* **UI Flow**:
  1. "Python, 3 years exp, Remote".
  2. Full JD generated.

## 222. Resume Screener
* **Description**: Scores resumes against a job description.
* **Features**:
  * Skill matching.
  * Blind screening (anonymization).
* **Requirements**:
  * **Models**: Embedding similarity.
* **UI Flow**:
  1. Upload Zip of resumes.
  2. Ranked list of candidates.

## 223. Interview Question Generator
* **Description**: Generates tailored interview questions based on candidate's resume and role.
* **Features**:
  * Behavioral questions.
  * Technical challenges.
* **Requirements**:
  * **Models**: LLM.
* **UI Flow**:
  1. Candidate profile view.
  2. "Ask about their gap year in 2020."

## 224. Meeting Scheduler (Business)
* **Description**: AI assistant that coordinates meeting times for teams.
* **Features**:
  * "Best time" finding.
  * Room booking.
* **Requirements**:
  * **Integration**: Calendar APIs.
* **UI Flow**:
  1. Slack: "@Scheduler find time for team sync".
  2. "Tuesday 2pm works for everyone."

## 225. RFP Response Generator
* **Description**: Drafts answers to Request for Proposal (RFP) questionnaires using a knowledge base.
* **Features**:
  * "Security Question" auto-fill.
  * Review workflow.
* **Requirements**:
  * **Models**: RAG.
* **UI Flow**:
  1. Upload Excel RFP.
  2. Download filled Excel.

## 226. Churn Predictor Service
* **Description**: Predicts which customers are likely to cancel their subscription.
* **Features**:
  * Feature importance (Why?).
  * Intervention suggestion.
* **Requirements**:
  * **Models**: Random Forest / Logistic Regression.
* **UI Flow**:
  1. CRM widget.
  2. "High Churn Risk. Offer 10% discount?"

## 227. Customer Lifetime Value (CLV) Estimator
* **Description**: Predicts the total future value of a customer.
* **Features**:
  * Cohort analysis.
* **Requirements**:
  * **Models**: Pareto/NBD models.
* **UI Flow**:
  1. User profile.
  2. "Predicted CLV: $5,000".

## 228. Dynamic Pricing Engine
* **Description**: Adjusts prices in real-time based on demand, inventory, and competition.
* **Features**:
  * Surge pricing logic.
  * Margin protection.
* **Requirements**:
  * **Models**: Reinforcement Learning.
* **UI Flow**:
  1. E-commerce admin.
  2. "Suggested Price: $24.99 (up from $19.99)".

## 229. Supply Chain Optimization Service
* **Description**: Predicts inventory needs and optimizes ordering schedules.
* **Features**:
  * Lead time forecasting.
  * Safety stock calculation.
* **Requirements**:
  * **Models**: Time-series forecasting.
* **UI Flow**:
  1. Dashboard.
  2. "Reorder Widgets now to avoid stockout in 2 weeks."

## 230. Legal Chatbot
* **Description**: First-line support for legal queries within a company.
* **Features**:
  * "Can I sign this?"
  * Policy retrieval.
* **Requirements**:
  * **Models**: RAG on Policy Docs.
* **UI Flow**:
  1. Slack bot.
  2. "Check the Travel Policy here."

## 231. Patent Drafter Assistant
* **Description**: Helps draft the claims and description sections of a patent application.
* **Features**:
  * Legalese generation.
  * Figure description.
* **Requirements**:
  * **Models**: Fine-tuned Legal LLM.
* **UI Flow**:
  1. Describe invention details.
  2. Generate "Claim 1".

## 232. GDPR Data Request Handler
* **Description**: Automates the collection of user data for Subject Access Requests (SAR).
* **Features**:
  * System-wide search.
  * Zip generation.
* **Requirements**:
  * **Integration**: DB connectors.
* **UI Flow**:
  1. Admin panel "Execute SAR for user@email.com".
  2. Download result.

## 233. Corporate Entity Resolution
* **Description**: Matches messy company names to legal entities (e.g., "IBM", "I.B.M.", "Intl Business Machines").
* **Features**:
  * DUNS number matching.
  * Hierarchy mapping.
* **Requirements**:
  * **Models**: Fuzzy matching / Dedupe.
* **UI Flow**:
  1. Upload dirty CSV.
  2. Download clean CSV with IDs.

## 234. Board Deck Generator
* **Description**: Generates slides for board meetings from financial data and updates.
* **Features**:
  * Chart generation.
  * Bullet point synthesis.
* **Requirements**:
  * **Integration**: PPTX generation.
* **UI Flow**:
  1. Connect metrics dashboard.
  2. Generate 10-slide deck.

## 235. Insider Threat Detector
* **Description**: Analyzes employee behavior to detect malicious insiders.
* **Features**:
  * Data exfiltration detection.
  * Abnormal login times.
* **Requirements**:
  * **Models**: Anomaly detection.
* **UI Flow**:
  1. Security Alert: "User downloaded 5GB of source code."

## 236. Payroll Error Detector
* **Description**: Validates payroll data before processing to find anomalies.
* **Features**:
  * Salary spike detection.
  * Ghost employee detection.
* **Requirements**:
  * **Models**: Statistical checks.
* **UI Flow**:
  1. Upload Payroll CSV.
  2. "Warning: John Doe salary +200%".

## 237. Vendor Risk Monitor
* **Description**: Continuously monitors vendors for financial health and security risks.
* **Features**:
  * News scraping.
  * Credit score monitoring.
* **Requirements**:
  * **Data**: External feeds.
* **UI Flow**:
  1. "Vendor Alert: Supplier X filed Ch 11 bankruptcy".

## 238. Real Estate Valuation (AVM)
* **Description**: Automated Valuation Model for properties.
* **Features**:
  * Comp analysis.
  * Image quality adjustment.
* **Requirements**:
  * **Models**: Regression + Vision.
* **UI Flow**:
  1. Address input.
  2. "Est Value: $450,000".

## 239. Lease Abstractor
* **Description**: Summarizes key dates and financial obligations from lease agreements.
* **Features**:
  * Rent ladder extraction.
  * Renewal option detection.
* **Requirements**:
  * **Models**: NLP.
* **UI Flow**:
  1. Upload Lease PDF.
  2. Dashboard with critical dates.

## 240. E-Discovery Service
* **Description**: Searches through massive volumes of emails/docs for litigation.
* **Features**:
  * Concept search.
  * Email threading.
* **Requirements**:
  * **Models**: Clustering / Search.
* **UI Flow**:
  1. "Find all emails about 'Project X'".
  2. Filter by "Privileged".

## 241. M&A Due Diligence Assistant
* **Description**: Accelerates the review of data room documents.
* **Features**:
  * Red flag detection.
  * Q&A generation.
* **Requirements**:
  * **Models**: Analysis agents.
* **UI Flow**:
  1. Connect to Data Room.
  2. "Summary of IP ownership".

## 242. Employee Sentiment Analyzer
* **Description**: Analyzes anonymous feedback or public reviews (Glassdoor) to gauge morale.
* **Features**:
  * Topic modeling (e.g., "Management", "Compensation").
* **Requirements**:
  * **Models**: Sentiment.
* **UI Flow**:
  1. HR Dashboard.
  2. "Sentiment trend: Down (Topic: Return to Office)".

## 243. Shift Scheduling Optimizer
* **Description**: Generates optimal shift schedules for hourly workers.
* **Features**:
  * Availability constraints.
  * Fairness balancing.
* **Requirements**:
  * **Models**: Constraint Solver (OR).
* **UI Flow**:
  1. "Generate Next Week".
  2. Calendar grid.

## 244. Sales Call Coach
* **Description**: Analyzes recordings of sales calls to provide feedback.
* **Features**:
  * "Talk-to-listen" ratio.
  * Objection handling scoring.
* **Requirements**:
  * **Models**: ASR + NLP.
* **UI Flow**:
  1. Sales rep dashboard.
  2. "Tip: Ask more open-ended questions."

## 245. Customer Segmentation Service
* **Description**: Clusters customers into personas based on behavior and demographics.
* **Features**:
  * Unsupervised clustering.
  * Persona naming.
* **Requirements**:
  * **Models**: K-Means / DBSCAN.
* **UI Flow**:
  1. Visualization of clusters.
  2. "Segment A: High Value / Low Frequency".

## 246. Brand Sentiment Monitor
* **Description**: Tracks brand perception across social media and web.
* **Features**:
  * Net Sentiment Score.
  * Crisis alert.
* **Requirements**:
  * **Models**: Social listening.
* **UI Flow**:
  1. Real-time ticker.
  2. "Brand health: 85/100".

## 247. Influencer Vetting Service
* **Description**: Analyzes influencer profiles for fake followers and brand alignment.
* **Features**:
  * Engagement rate verification.
  * Content safety check.
* **Requirements**:
  * **Models**: Anomaly detection.
* **UI Flow**:
  1. Input Instagram handle.
  2. "Fake Followers: 45% (High Risk)".

## 248. Ad Bid Optimizer
* **Description**: Automates bidding on ad platforms to maximize ROAS.
* **Features**:
  * Real-time bid adjustment.
  * Budget pacing.
* **Requirements**:
  * **Models**: RL / Regression.
* **UI Flow**:
  1. "Target CPA: $10".
  2. Auto-pilot enabled.

## 249. SEO Content Brief Generator
* **Description**: Generates detailed outlines for content writers based on SERP analysis.
* **Features**:
  * Competitor header analysis.
  * "People also ask" integration.
* **Requirements**:
  * **Models**: Search + Summarization.
* **UI Flow**:
  1. Keyword "Best CRM".
  2. Brief: "Title: Top 10 CRMs... H2: What is CRM?..."

## 250. Logo Compliance Checker
* **Description**: Checks images to ensure brand logos are used correctly (spacing, color).
* **Features**:
  * Brand guideline enforcement.
* **Requirements**:
  * **Models**: Vision.
* **UI Flow**:
  1. Upload marketing asset.
  2. "Error: Logo clear space violated."
