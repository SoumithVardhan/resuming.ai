
import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Loader2, ArrowLeft, Lightbulb, CheckCircle, TrendingUp, FileText, Target } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useToast } from "@/hooks/use-toast";

interface ResumePoint {
  original_point: string;
  enhanced_point: string;
}

interface EnhancementResponse {
  enhanced_resume_points: ResumePoint[];
  recommendations: string[];
}

const ResumeEnhancer = () => {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<EnhancementResponse | null>(null);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!resume.trim() || !jobDescription.trim()) {
      toast({
        title: "Missing Information",
        description: "Please provide both your resume and the job description.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      // Simulate API call for demo
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Mock response for demonstration
      const mockResponse: EnhancementResponse = {
        enhanced_resume_points: [
          {
            original_point: "Built a web application using React and Node.js",
            enhanced_point: "Built a scalable web application using React, Node.js, and AWS services (EC2, S3) with microservices architecture, implementing CI/CD pipelines for automated deployment"
          },
          {
            original_point: "Developed data processing system",
            enhanced_point: "Developed cloud-native data processing system on AWS Lambda processing 1M+ records daily, utilizing Docker containers and Infrastructure as Code (Terraform) for reliable deployment"
          },
          {
            original_point: "Created REST API for mobile app",
            enhanced_point: "Created high-performance REST API serving 10K+ requests per minute using Python and microservices architecture, deployed on Kubernetes with automated CI/CD pipelines"
          }
        ],
        recommendations: [
          "Add specific AWS services experience (EC2, Lambda, S3) as these are explicitly required in the job description",
          "Include Kubernetes orchestration experience with specific cluster management or deployment examples",
          "Highlight CI/CD pipeline implementation with tools like Jenkins, GitLab CI, or GitHub Actions",
          "Add Infrastructure as Code experience using Terraform for AWS resource management",
          "Quantify Agile/Scrum experience with team size and sprint delivery metrics"
        ]
      };
      
      setResults(mockResponse);
      
      toast({
        title: "Enhancement Complete!",
        description: "Your resume has been successfully enhanced with AI insights.",
      });
      
    } catch (error) {
      toast({
        title: "Enhancement Failed",
        description: "There was an error processing your request. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="w-full px-6 py-4 border-b bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <ArrowLeft className="w-5 h-5 text-gray-600" />
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">ResumeAI</span>
            </div>
          </Link>
          <Badge variant="secondary" className="bg-green-100 text-green-800">
            Free Tool
          </Badge>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-8 max-w-7xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Resume Enhancement Tool
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Paste your resume and target job description to get AI-powered enhancements and recommendations
          </p>
        </div>

        {!results ? (
          <form onSubmit={handleSubmit} className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card className="h-fit">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <FileText className="w-5 h-5 text-blue-600" />
                    <span>Your Current Resume</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Label htmlFor="resume" className="text-sm font-medium text-gray-700 mb-2 block">
                    Paste your resume content below
                  </Label>
                  <Textarea
                    id="resume"
                    value={resume}
                    onChange={(e) => setResume(e.target.value)}
                    className="min-h-[400px] text-sm"
                    placeholder="John Doe
Software Engineer

Skills: Python, JavaScript, React, Node.js, SQL

Projects:
• Built a scalable web application using React and Node.js
• Developed data pipeline processing 1M records daily
• Created REST API serving 10K requests per minute

Experience:
• Software Engineer at TechCorp (2020-2023)
• Implemented microservices architecture
• Reduced API response time by 40%"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Include your skills, projects, and experience sections for best results
                  </p>
                </CardContent>
              </Card>

              <Card className="h-fit">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Target className="w-5 h-5 text-purple-600" />
                    <span>Target Job Description</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Label htmlFor="jobDescription" className="text-sm font-medium text-gray-700 mb-2 block">
                    Paste the job description you're targeting
                  </Label>
                  <Textarea
                    id="jobDescription"
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    className="min-h-[400px] text-sm"
                    placeholder="Senior Software Engineer - Cloud Platform

Required:
- 5+ years Python experience
- Strong knowledge of AWS services (EC2, Lambda, S3)
- Experience with microservices and REST APIs
- Docker and Kubernetes experience
- CI/CD pipeline expertise

Preferred:
- React and modern JavaScript
- Infrastructure as Code (Terraform)
- Agile/Scrum experience

Responsibilities:
• Design and implement scalable cloud solutions
• Build and maintain microservices architecture
• Implement CI/CD pipelines and DevOps practices
• Collaborate with cross-functional teams in Agile environment"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Include requirements, preferred skills, and responsibilities for best matching
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="text-center">
              <Button
                type="submit"
                disabled={loading}
                size="lg"
                className="text-lg px-12 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Analyzing & Enhancing...
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-5 h-5 mr-2" />
                    Enhance My Resume
                  </>
                )}
              </Button>
              {loading && (
                <p className="text-sm text-gray-600 mt-2">
                  AI is analyzing your resume against job requirements and similar successful profiles...
                </p>
              )}
            </div>
          </form>
        ) : (
          <div className="space-y-8">
            {/* Enhanced Points Section */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-2xl">
                  <TrendingUp className="w-6 h-6 text-green-600" />
                  <span>Enhanced Resume Points</span>
                  <Badge variant="secondary" className="ml-2 bg-green-100 text-green-800">
                    {results.enhanced_resume_points.length} points enhanced
                  </Badge>
                </CardTitle>
                <p className="text-gray-600">
                  Your bullet points have been enhanced with relevant keywords and improved structure
                </p>
              </CardHeader>
              <CardContent className="space-y-6">
                {results.enhanced_resume_points.map((point, index) => (
                  <div key={index} className="border rounded-lg p-6 bg-gradient-to-r from-gray-50 to-blue-50">
                    <div className="mb-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="text-sm font-medium text-gray-500">ORIGINAL:</span>
                        <Badge variant="outline" className="text-xs">Before</Badge>
                      </div>
                      <p className="text-gray-700 bg-white p-3 rounded border border-gray-200">
                        {point.original_point}
                      </p>
                    </div>
                    <div>
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="text-sm font-medium text-green-700">ENHANCED:</span>
                        <Badge className="text-xs bg-green-100 text-green-800">After</Badge>
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      </div>
                      <p className="text-gray-900 bg-green-50 p-3 rounded border border-green-200 font-medium">
                        {point.enhanced_point}
                      </p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Recommendations Section */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-2xl">
                  <Lightbulb className="w-6 h-6 text-yellow-600" />
                  <span>AI Recommendations</span>
                  <Badge variant="secondary" className="ml-2 bg-yellow-100 text-yellow-800">
                    {results.recommendations.length} insights
                  </Badge>
                </CardTitle>
                <p className="text-gray-600">
                  Personalized suggestions to further improve your resume's impact
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {results.recommendations.map((recommendation, index) => (
                    <div key={index} className="flex items-start space-x-3 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <div className="w-6 h-6 bg-yellow-200 text-yellow-800 rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0 mt-0.5">
                        {index + 1}
                      </div>
                      <p className="text-gray-800 leading-relaxed">{recommendation}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                onClick={() => {
                  setResults(null);
                  setResume('');
                  setJobDescription('');
                }}
                variant="outline"
                size="lg"
                className="px-8"
              >
                Enhance Another Resume
              </Button>
              <Button
                onClick={() => {
                  const content = `ENHANCED RESUME POINTS:\n\n${results.enhanced_resume_points.map((point, i) => 
                    `${i + 1}. ${point.enhanced_point}`
                  ).join('\n\n')}\n\nRECOMMENDATIONS:\n\n${results.recommendations.map((rec, i) => 
                    `${i + 1}. ${rec}`
                  ).join('\n\n')}`;
                  
                  navigator.clipboard.writeText(content);
                  toast({
                    title: "Copied to Clipboard!",
                    description: "Enhancement results copied to your clipboard.",
                  });
                }}
                size="lg"
                className="px-8 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                Copy Results
              </Button>
            </div>

            <Separator className="my-8" />

            {/* Tips Section */}
            <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
              <CardHeader>
                <CardTitle className="text-lg text-blue-900">💡 Next Steps</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-blue-800">
                  <li>• Update your resume with the enhanced bullet points</li>
                  <li>• Work on the recommended skills and experiences</li>
                  <li>• Tailor your resume for each specific job application</li>
                  <li>• Use keywords naturally throughout your resume</li>
                  <li>• Keep your resume updated with new achievements</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeEnhancer;
