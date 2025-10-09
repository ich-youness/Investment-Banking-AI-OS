import { useNavigate } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { 
  Calculator,
  Building2,
  TrendingUp,
  DollarSign,
  Brain,
  Users
} from "lucide-react";

const teams = [
  { 
    id: "company_valuation", 
    name: "Company Valuation", 
    icon: Calculator, 
    description: "AI-powered corporate valuation using Asset-Based, Market-Based, and Earning-Based approaches" 
  },
  // { 
  //   id: "company_valuation_v2", 
  //   name: "Advanced Company Valuation", 
  //   icon: Users, 
  //   description: "Multi-agent financial analysis system with specialized analysts for comprehensive company evaluation" 
  // }
];

const Landing = () => {
  const navigate = useNavigate();

  const handleTeamClick = (teamId: string) => {
    navigate(`/team/${teamId}`);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-first-color py-8 px-6 shadow-lg">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-fourth-color mb-4">
            Team Hub
          </h1>
          <p className="text-xl text-fourth-color/80 max-w-2xl mx-auto">
            Connect with specialized teams and their AI agents to get instant help and collaboration
          </p>
        </div>
      </header>

      {/* Teams Grid */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {teams.map((team) => {
            const IconComponent = team.icon;
            return (
              <Card
                key={team.id}
                className="bg-second-color border-0 hover:bg-third-color transition-smooth cursor-pointer transform hover:scale-105 shadow-lg hover:shadow-xl"
                onClick={() => handleTeamClick(team.id)}
              >
                <CardContent className="p-6 text-center">
                  <div className="mb-4 flex justify-center">
                    <IconComponent className="h-12 w-12 text-fourth-color" />
                  </div>
                  <h3 className="text-xl font-semibold text-fourth-color mb-2">
                    {team.name}
                  </h3>
                  <p className="text-fourth-color/70">
                    {team.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default Landing;