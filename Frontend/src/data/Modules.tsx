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
  Settings
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

export const allTeams = [
  companyValuationTeam
];
