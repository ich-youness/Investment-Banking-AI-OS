import { 
  Calculator, 
  FileText, 
  Target,
  Database,
  TrendingUp,
  Building2,
  Activity,
  DollarSign,
  ChartBar,
  BarChart,
  PieChart,
  Brain,
  Search,
  CheckCircle,
  AlertCircle,
  Eye,
  Settings,
  Users,
  TrendingDown,
  PieChart as PieChartIcon,
  BarChart3
} from "lucide-react";

export interface Agent {
  id: string;
  name: string;
  description: string;
  icon: any;
  outputs: string[];
}

export interface SubTeam {
  id: string;
  name: string;
  description: string;
  mode: string;
  icon: any;
  agents: Agent[];
}

export interface Team {
  id: string;
  name: string;
  description: string;
  icon: any;
  subTeams: SubTeam[];
}

// Company Valuation Module
export const companyValuationTeam: Team = {
  id: "company_valuation",
  name: "Company Valuation",
  description: "AI-powered corporate valuation using Asset-Based, Market-Based, and Earning-Based approaches",
          icon: Calculator,
  subTeams: [
    {
      id: "valuation-analysis",
      name: "Valuation Analysis",
      description: "Comprehensive company valuation using multiple approaches and tools",
      mode: "Coordinate",
      icon: Calculator,
      agents: [
        {
          id: "financial_data_agent",
          name: "Financial Data Agent",
          description: "Expert AI financial analyst specializing in corporate and M&A valuations. Performs Asset-Based, Market-Based, and Earning-Based valuations using advanced financial tools and generates comprehensive valuation reports.",
          icon: Calculator,
          outputs: [
            "Asset-Based Valuations (Book Value, Liquidation Value)",
            "Market-Based Valuations (Market Cap, Comparable Multiples)",
            "Earning-Based Valuations (DCF, Earnings Multiples)",
            "Triangulated Valuation Reports",
            "Peer Discovery and Analysis",
            "Financial Statement Analysis",
            "Valuation Confidence Scores",
            "Scenario Analysis and Sensitivity Testing"
          ]
        }
      ]
    }
  ]
};

// export const fipAITeam: Team = {
//   id: "fip-ai",
//   name: "FIP AI Team",
//   description: "AI-powered Financial Insurance Platform agents for data processing, financial calculations, and scenario management",
//   icon: Building2,
//   subTeams: [
//     {
//       id: "data-processing",
//       name: "Data Processing",
//       description: "Data reading, validation, and transformation for FIP system",
//       mode: "Coordinate",
//       icon: Database,
//       agents: [
//         {
//           id: "data-processing-agent",
//           name: "Data Processing Agent",
//           description: "FIP Data Processing and Management Expert - Handle data reading, validation, and transformation for the FIP system. Manage RIC and SCG data for both P&C and L&H business units.",
//           icon: Database,
//           outputs: [
//             "Clean RIC & SCG Data",
//             "Data Quality Reports",
//             "Validated Financial Metrics",
//             "Processed Data Files",
//             "Data Transformation Results"
//           ]
//         }
//       ]
//     },
//     {
//       id: "financial-calculations",
//       name: "Financial Calculations",
//       description: "Complex financial calculations, equity projections, and financial modeling",
//       mode: "Coordinate",
//       icon: Calculator,
//       agents: [
//         {
//           id: "financial-calculations-agent",
//           name: "Financial Calculations Agent",
//           description: "FIP Financial Calculations and Modeling Expert - Perform complex financial calculations, equity projections, allocations, and financial modeling. Handle BU splits, EoF calculations, and SCG processing.",
//           icon: Calculator,
//           outputs: [
//             "Equity Projections",
//             "BU Split Calculations",
//             "EoF Calculations",
//             "Financial Ratios",
//             "Capital Requirements"
//           ]
//         }
//       ]
//     },
//     {
//       id: "scenario-management",
//       name: "Scenario Management",
//       description: "Scenario calculations, sensitivity analysis, and what-if modeling",
//       mode: "Coordinate",
//       icon: Activity,
//       agents: [
//         {
//           id: "scenario-management-agent",
//           name: "Scenario Management Agent",
//           description: "FIP Scenario Analysis and Sensitivity Testing Expert - Handle scenario calculations, sensitivity analysis, and what-if modeling. Process multiple scenarios, apply shocks, and perform stress testing.",
//           icon: Activity,
//           outputs: [
//             "Scenario Analysis Reports",
//             "Sensitivity Analysis Results",
//             "Stress Test Reports",
//             "What-If Modeling Outputs",
//             "Risk Assessment Reports"
//           ]
//         }
//       ]
//     }
//   ]
// };

// Company Valuation V2 Module (Multi-Agent System)
// export const companyValuationV2Team: Team = {
//   id: "company_valuation_v2",
//   name: "Advanced Company Valuation",
//   description: "Multi-agent financial analysis system with specialized analysts for comprehensive company evaluation",
//   icon: Users,
//   subTeams: [
//     {
//       id: "financial-analysis-team",
//       name: "Financial Analysis Team",
//       description: "Specialized financial analysts working together for comprehensive company evaluation",
//       mode: "Coordinate",
//       icon: Users,
//       agents: [
//         {
//           id: "income_statement_analyst",
//           name: "Income Statement Analyst",
//           description: "Specialized in analyzing revenue growth trends, calculating key margins (gross, operating, net), analyzing EBITDA and operating performance, and identifying trends in profitability and operational efficiency.",
//           icon: TrendingUp,
//           outputs: [
//             "Revenue Growth Analysis",
//             "Margin Analysis (Gross, Operating, Net)",
//             "EBITDA Performance Assessment",
//             "Profitability Trend Analysis",
//             "Cost Structure Evaluation",
//             "Quarter-over-Quarter Analysis",
//             "Year-over-Year Comparisons",
//             "Industry Benchmarking"
//           ]
//         },
//         {
//           id: "balance_sheet_analyst",
//           name: "Balance Sheet Analyst",
//           description: "Expert in analyzing capital structure, assessing liquidity position, evaluating financial health, and analyzing asset quality and composition for solvency and financial stability assessment.",
//           icon: BarChart3,
//           outputs: [
//             "Capital Structure Analysis",
//             "Debt-to-Equity Ratios",
//             "Liquidity Position Assessment",
//             "Current & Quick Ratios",
//             "Financial Health Evaluation",
//             "Asset Quality Analysis",
//             "Working Capital Analysis",
//             "Solvency Assessment"
//           ]
//         },
//         {
//           id: "valuation_analyst",
//           name: "Valuation Analyst",
//           description: "Specialized in valuation by multiples, calculating Enterprise Value, applying appropriate industry multiples, performing comparable company analysis, and providing valuation ranges with sensitivity analysis.",
//           icon: DollarSign,
//           outputs: [
//             "Enterprise Value Calculations",
//             "Multiples Analysis (EV/Revenue, EV/EBITDA, P/E, P/B)",
//             "Comparable Company Analysis",
//             "Industry Benchmarking",
//             "Valuation Range Estimates",
//             "Sensitivity Analysis",
//             "Fair Value Assessment",
//             "Investment Recommendations"
//           ]
//         },
//         {
//           id: "chief_financial_analyst",
//           name: "Chief Financial Analyst",
//           description: "Master coordinator that synthesizes findings from all specialist agents, provides comprehensive company valuation and investment recommendations, and identifies interconnections between different analysis domains.",
//           icon: Brain,
//           outputs: [
//             "Integrated Financial Analysis",
//             "Comprehensive Valuation Reports",
//             "Investment Recommendations",
//             "Risk Assessment",
//             "Opportunity Identification",
//             "Cross-Domain Insights",
//             "Executive Summary",
//             "Strategic Recommendations"
//           ]
//         }
//       ]
//     }
//   ]
// };

export const allTeams = [
  companyValuationTeam,
  // companyValuationV2Team
];
