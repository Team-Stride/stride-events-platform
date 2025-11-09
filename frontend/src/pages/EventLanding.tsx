import { Button } from "@/components/ui/button";
import { useParams } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import { eventApi, type StudentRegistration, type SchoolRegistration } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useState } from "react";
import { toast } from "sonner";
import { 
  Loader2, Trophy, Users, Award, Calendar, GraduationCap, 
  ArrowRight, Brain, Target, Rocket, Lightbulb, CheckCircle2,
  BookOpen, Briefcase, TrendingUp, Building2, User
} from "lucide-react";

export default function EventLanding() {
  const { slug } = useParams<{ slug: string }>();
  
  const eventSlug = slug || "ai-olympiad-2025";
  const { data: event, isLoading } = useQuery({
    queryKey: ['event', eventSlug],
    queryFn: () => eventApi.getBySlug(eventSlug),
    enabled: !!eventSlug,
  });
  
  const [studentDialogOpen, setStudentDialogOpen] = useState(false);
  const [schoolDialogOpen, setSchoolDialogOpen] = useState(false);

  const registerStudentMutation = useMutation({
    mutationFn: (data: StudentRegistration) => 
      eventApi.registerStudent(event?.id || 1, data),
    onSuccess: () => {
      toast.success("Registration successful! Check your email for confirmation.");
      setStudentDialogOpen(false);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Registration failed. Please try again.");
    },
  });

  const registerSchoolMutation = useMutation({
    mutationFn: (data: SchoolRegistration) => 
      eventApi.registerSchool(event?.id || 1, data),
    onSuccess: (data: any) => {
      toast.success(`School registered! Your unique ID: ${data.unique_school_id || 'Check email'}`);
      setSchoolDialogOpen(false);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "School registration failed.");
    },
  });

  const handleStudentSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    registerStudentMutation.mutate({
      eventId: event!.id,
      firstName: formData.get("firstName") as string,
      lastName: formData.get("lastName") as string,
      email: formData.get("email") as string,
      mobile: formData.get("mobile") as string,
      grade: formData.get("grade") as string,
      schoolName: formData.get("schoolName") as string,
      city: formData.get("city") as string,
      state: formData.get("state") as string,
    });
  };

  const handleSchoolSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    registerSchoolMutation.mutate({
      schoolName: formData.get("schoolName") as string,
      contactPerson: formData.get("contactPerson") as string,
      contactEmail: formData.get("contactEmail") as string,
      contactMobile: formData.get("contactMobile") as string,
      city: formData.get("city") as string,
      state: formData.get("state") as string,
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (!event) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Event Not Found</h1>
          <Button onClick={() => navigate("/")}>Go Home</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)',
            backgroundSize: '40px 40px'
          }}></div>
        </div>

        <div className="relative container py-20 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="inline-block">
                <span className="bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm font-medium">
                  🏆 India's Premier AI Competition for Students
                </span>
              </div>

              <h1 className="text-4xl lg:text-5xl font-bold leading-tight">
                AI Olympiad: The NextGen AI Challenge
                <span className="block text-blue-200 mt-2">2025</span>
              </h1>

              <p className="text-xl lg:text-2xl text-blue-100 leading-relaxed">
                Where Artificial Intelligence Meets Human Imagination
              </p>

              <div className="flex flex-wrap gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <Calendar className="w-5 h-5" />
                  <span>Registration Closes: 31st December 2025</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  <span>Open to Grades 9-12</span>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  size="lg"
                  onClick={() => setStudentDialogOpen(true)}
                  className="group bg-white text-blue-700 hover:bg-blue-50 text-lg px-8 shadow-xl hover:shadow-2xl hover:scale-105 transition-all"
                >
                  Register Now - ₹99
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-white text-white hover:bg-white/10 text-lg px-8"
                >
                  Learn More
                </Button>
              </div>

              <p className="text-sm text-blue-200">
                💡 Use code <span className="font-bold text-white bg-blue-500/30 px-2 py-1 rounded">KEEPSTRIDING</span> for 100% discount!
              </p>
            </div>

            <div className="relative lg:block hidden">
              <div className="relative h-96 bg-white/10 backdrop-blur-sm rounded-2xl border-2 border-white/20 flex items-center justify-center">
                <div className="text-center space-y-4">
                  <div className="text-6xl">🤖</div>
                  <p className="text-white/80">Hero Image / Video</p>
                  <p className="text-sm text-white/60">1920×1080px (16:9)</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z" fill="white"/>
          </svg>
        </div>
      </section>

      {/* What is AI Olympiad Section */}
      <section className="container py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">What is the AI Olympiad?</h2>
          <p className="text-xl text-gray-700 leading-relaxed mb-8">
            The <strong>Stride Ahead AI Olympiad</strong> is India's most prestigious artificial intelligence competition designed exclusively for high school students in Grades 9-12. This groundbreaking event aims to identify, nurture, and celebrate young minds passionate about AI and emerging technologies.
          </p>
          <p className="text-lg text-gray-600 leading-relaxed mb-8">
            Through a carefully crafted assessment covering AI fundamentals, machine learning concepts, ethical considerations, and real-world applications, participants will demonstrate their understanding of one of the most transformative technologies of our time. Whether you're an AI enthusiast or just beginning your journey, this Olympiad offers an unparalleled platform to test your knowledge, compete with peers nationwide, and gain recognition from industry leaders.
          </p>
          <div className="grid md:grid-cols-3 gap-6 mt-12">
            <Card className="p-6 text-center hover:shadow-lg transition-shadow">
              <Brain className="w-12 h-12 mx-auto mb-4 text-blue-600" />
              <h3 className="font-bold text-lg mb-2">AI Fundamentals</h3>
              <p className="text-sm text-gray-600">Core concepts, algorithms, and applications</p>
            </Card>
            <Card className="p-6 text-center hover:shadow-lg transition-shadow">
              <Target className="w-12 h-12 mx-auto mb-4 text-purple-600" />
              <h3 className="font-bold text-lg mb-2">Real-World Problems</h3>
              <p className="text-sm text-gray-600">Practical AI solutions and case studies</p>
            </Card>
            <Card className="p-6 text-center hover:shadow-lg transition-shadow">
              <Lightbulb className="w-12 h-12 mx-auto mb-4 text-yellow-600" />
              <h3 className="font-bold text-lg mb-2">Ethical AI</h3>
              <p className="text-sm text-gray-600">Responsible AI development and deployment</p>
            </Card>
          </div>

          {/* Event Information Table */}
          <div className="mt-16 max-w-2xl mx-auto">
            <Card className="overflow-hidden border-2 border-blue-200">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4">
                <h3 className="text-2xl font-bold text-center">Event Information</h3>
              </div>
              <div className="divide-y">
                <div className="grid grid-cols-2 p-4 hover:bg-gray-50 transition-colors">
                  <div className="font-semibold text-gray-700">Mode</div>
                  <div className="text-gray-900">100% Online</div>
                </div>
                <div className="grid grid-cols-2 p-4 hover:bg-gray-50 transition-colors">
                  <div className="font-semibold text-gray-700">Dates</div>
                  <div className="text-gray-900">December 15 – 25, 2025</div>
                </div>
                <div className="grid grid-cols-2 p-4 hover:bg-gray-50 transition-colors">
                  <div className="font-semibold text-gray-700">Participation Fee</div>
                  <div className="text-gray-900">₹99 (Use code KEEPSTRIDING for FREE)</div>
                </div>
                <div className="grid grid-cols-2 p-4 hover:bg-gray-50 transition-colors">
                  <div className="font-semibold text-gray-700">Attempt Window</div>
                  <div className="text-gray-900">Attempt anytime during Jan 15–25 — flexible & stress-free</div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* 4-Box Value Grid Section */}
      <section className="py-20 bg-white">
        <div className="container">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              <Card className="p-8 hover:shadow-xl transition-all border-2 border-blue-100 hover:border-blue-300">
                <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mb-6">
                  <span className="text-2xl font-bold text-blue-600">1</span>
                </div>
                <Trophy className="w-10 h-10 mb-4 text-blue-600" />
                <h3 className="text-xl font-bold mb-3">Rewards & Recognition</h3>
                <p className="text-sm font-semibold text-gray-700 mb-2">Prizes • Trophies • National AI Innovator Titles</p>
                <p className="text-gray-600 text-sm">Students earn national-level recognition and build academic prestige through awards that matter.</p>
              </Card>

              <Card className="p-8 hover:shadow-xl transition-all border-2 border-purple-100 hover:border-purple-300">
                <div className="w-14 h-14 bg-purple-100 rounded-full flex items-center justify-center mb-6">
                  <span className="text-2xl font-bold text-purple-600">2</span>
                </div>
                <Users className="w-10 h-10 mb-4 text-purple-600" />
                <h3 className="text-xl font-bold mb-3">Mentorship from AI Game-Changers</h3>
                <p className="text-sm font-semibold text-gray-700 mb-2">Industry Experts • Innovators • Startup Leaders</p>
                <p className="text-gray-600 text-sm">Learn directly from AI pioneers shaping global technology and innovation.</p>
              </Card>

              <Card className="p-8 hover:shadow-xl transition-all border-2 border-green-100 hover:border-green-300">
                <div className="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mb-6">
                  <span className="text-2xl font-bold text-green-600">3</span>
                </div>
                <GraduationCap className="w-10 h-10 mb-4 text-green-600" />
                <h3 className="text-xl font-bold mb-3">Achievements That Build Profiles</h3>
                <p className="text-sm font-semibold text-gray-700 mb-2">Certificates • Digital Badges • College-Ready Credentials</p>
                <p className="text-gray-600 text-sm">Every participant receives verifiable credentials that enhance portfolios and college applications.</p>
              </Card>

              <Card className="p-8 hover:shadow-xl transition-all border-2 border-orange-100 hover:border-orange-300">
                <div className="w-14 h-14 bg-orange-100 rounded-full flex items-center justify-center mb-6">
                  <span className="text-2xl font-bold text-orange-600">4</span>
                </div>
                <Rocket className="w-10 h-10 mb-4 text-orange-600" />
                <h3 className="text-xl font-bold mb-3">Future Opportunities & Global Exposure</h3>
                <p className="text-sm font-semibold text-gray-700 mb-2">Internships • Mentorships • National & Global Visibility</p>
                <p className="text-gray-600 text-sm">Top performers join the Stride Network for extended learning and innovation opportunities.</p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Why Participate Section */}
      <section className="py-20 bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="container">
          <h2 className="text-4xl lg:text-5xl font-bold text-center mb-6">💡 WHY PARTICIPATE</h2>
          <div className="max-w-4xl mx-auto space-y-6">
            <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-blue-500">
              <div className="flex items-start gap-4">
                <Brain className="w-8 h-8 text-blue-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-bold mb-2">Learn Future-Ready Skills</h3>
                  <p className="text-gray-600">Explore AI, Machine Learning, and Innovation Thinking through gamified challenges.</p>
                </div>
              </div>
            </Card>
            <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-yellow-500">
              <div className="flex items-start gap-4">
                <Trophy className="w-8 h-8 text-yellow-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-bold mb-2">Win National Recognition</h3>
                  <p className="text-gray-600">₹1 Lakh in cash prizes, trophies, and "India's Young AI Innovator" titles.</p>
                </div>
              </div>
            </Card>
            <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-green-500">
              <div className="flex items-start gap-4">
                <GraduationCap className="w-8 h-8 text-green-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-bold mb-2">Build a College-Ready Profile</h3>
                  <p className="text-gray-600">Certificates and badges that stand out on resumes and applications.</p>
                </div>
              </div>
            </Card>
            <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-purple-500">
              <div className="flex items-start gap-4">
                <TrendingUp className="w-8 h-8 text-purple-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-bold mb-2">Gain Lifelong Tools</h3>
                  <p className="text-gray-600">One-year access to StrideAhead's AI-powered dashboard for continued learning.</p>
                </div>
              </div>
            </Card>
            <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-red-500">
              <div className="flex items-start gap-4">
                <Award className="w-8 h-8 text-red-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-bold mb-2">Bring Pride to Your School</h3>
                  <p className="text-gray-600">Earn national media features and institutional recognition for innovation leadership.</p>
                </div>
              </div>
            </Card>
          </div>

          {/* CTA after Why Participate */}
          <div className="mt-16 text-center">
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-8 border-2 border-blue-200">
              <p className="text-2xl font-bold text-gray-900 mb-4">
                Don't miss this opportunity to showcase your AI skills!
              </p>
              <p className="text-gray-600 mb-6 text-lg">Join thousands of students competing for ₹1 Lakh in prizes</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  size="lg" 
                  onClick={() => setStudentDialogOpen(true)}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-lg px-8"
                >
                  <User className="w-5 h-5 mr-2" />
                  Register as Student
                </Button>
                <Button 
                  size="lg" 
                  onClick={() => setSchoolDialogOpen(true)}
                  variant="outline"
                  className="border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white font-bold text-lg px-8"
                >
                  <Building2 className="w-5 h-5 mr-2" />
                  Register as School
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container py-20">
        <h2 className="text-4xl lg:text-5xl font-bold text-center mb-16">How It Works</h2>
        <div className="max-w-4xl mx-auto">
          <div className="space-y-8">
            {[
              { step: 1, title: "Register Online", desc: "Complete your registration by 31st December 2025. Pay ₹99 or use code KEEPSTRIDING for free entry.", icon: User },
              { step: 2, title: "Prepare & Practice", desc: "Access free study materials, sample questions, and AI learning resources on our platform. Olympiad window: December 15-25, 2025.", icon: BookOpen },
              { step: 3, title: "Get Results & Recognition", desc: "View instant results, download certificates, and unlock 1-year free access to the Stride Ahead Career Dashboard. Attempt window: January 15-25, 2025 (flexible & stress-free).", icon: Award },
              { step: 4, title: "Win & Celebrate", desc: "Winners announced on January 30, 2026. Top performers receive prizes, trophies, certificates, and national recognition!", icon: Trophy }
            ].map((item) => (
              <div key={item.step} className="flex gap-6 items-start">
                <div className="flex-shrink-0 w-16 h-16 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 text-white flex items-center justify-center text-2xl font-bold shadow-lg">
                  {item.step}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <item.icon className="w-6 h-6 text-blue-600" />
                    <h3 className="text-2xl font-bold">{item.title}</h3>
                  </div>
                  <p className="text-lg text-gray-600">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Prizes Section */}
      <section className="py-20 bg-gradient-to-br from-yellow-50 to-orange-50">
        <div className="container">
          <h2 className="text-4xl lg:text-5xl font-bold text-center mb-6">Prizes & Rewards</h2>
          <p className="text-xl text-center text-gray-600 mb-16 max-w-3xl mx-auto">
            Total prize pool worth ₹1,00,000 plus exclusive opportunities!
          </p>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="p-8 text-center relative overflow-hidden border-4 border-yellow-400 shadow-2xl">
              <div className="absolute top-0 right-0 bg-yellow-400 text-yellow-900 px-4 py-1 text-sm font-bold">
                Winner
              </div>
              <Trophy className="w-20 h-20 mx-auto mb-4 text-yellow-500" />
              <div className="mb-4">
                <h3 className="text-3xl font-bold">₹30,000</h3>
                <p className="text-sm font-semibold text-yellow-700 mt-1">India's Young AI Innovator 2025</p>
              </div>
              <ul className="text-left space-y-2 text-gray-700 text-sm">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Cash Prize of ₹30,000</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Incubation Support to develop skills further</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Personalized Mentorship Sessions with AI Experts</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Winner's Certificate & National Recognition Feature</span>
                </li>
              </ul>
            </Card>

            <Card className="p-8 text-center relative overflow-hidden border-4 border-gray-400 shadow-xl">
              <div className="absolute top-0 right-0 bg-gray-400 text-gray-900 px-4 py-1 text-sm font-bold">
                1st Runner-Up
              </div>
              <Trophy className="w-20 h-20 mx-auto mb-4 text-gray-400" />
              <h3 className="text-3xl font-bold mb-4">₹15,000</h3>
              <ul className="text-left space-y-2 text-gray-700 text-sm">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Cash Prize of ₹15,000</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Exclusive Mentorship Sessions with industry leaders</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Certificate of Excellence</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Feature on Stride Ahead Innovation Network</span>
                </li>
              </ul>
            </Card>

            <Card className="p-8 text-center relative overflow-hidden border-4 border-orange-400 shadow-xl">
              <div className="absolute top-0 right-0 bg-orange-400 text-orange-900 px-4 py-1 text-sm font-bold">
                2nd Runner-Up
              </div>
              <Trophy className="w-20 h-20 mx-auto mb-4 text-orange-400" />
              <h3 className="text-3xl font-bold mb-4">₹10,000</h3>
              <ul className="text-left space-y-2 text-gray-700 text-sm">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Cash Prize of ₹10,000</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Guided Mentorship Opportunities</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Certificate of Excellence</span>
                </li>
              </ul>
            </Card>
          </div>
          <div className="mt-12 text-center max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold mb-4">Certificates for All Participants</h3>
            <p className="text-gray-600">
              Every participant receives a <strong>National Certificate of Participation and Digital Badge</strong>, showcasing their effort, creativity, and AI aptitude — perfect for school records, portfolios, and college applications.
            </p>
          </div>

          {/* CTA after Prizes */}
          <div className="mt-16 text-center">
            <div className="bg-white rounded-2xl p-8 border-2 border-yellow-400 shadow-xl">
              <p className="text-3xl font-bold text-gray-900 mb-3">
                🏆 Compete for ₹1 Lakh in Prizes!
              </p>
              <p className="text-gray-600 mb-6 text-lg">Register today and get instant access to study materials</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  size="lg" 
                  onClick={() => setStudentDialogOpen(true)}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold text-lg px-8 shadow-lg"
                >
                  <User className="w-5 h-5 mr-2" />
                  Register as Student
                </Button>
                <Button 
                  size="lg" 
                  onClick={() => setSchoolDialogOpen(true)}
                  variant="outline"
                  className="border-2 border-purple-600 text-purple-600 hover:bg-purple-600 hover:text-white font-bold text-lg px-8"
                >
                  <Building2 className="w-5 h-5 mr-2" />
                  Register as School
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Judging Criteria Section */}
      <section className="py-20 bg-gradient-to-br from-purple-50 to-blue-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl lg:text-5xl font-bold text-center mb-6">JUDGING CRITERIA</h2>
            <p className="text-xl text-center text-gray-700 mb-12">
              Every participant's performance will be evaluated on:
            </p>
            <div className="space-y-6">
              <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-blue-500">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-lg font-bold text-blue-600">1</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Concept Understanding</h3>
                    <p className="text-gray-600">Clarity of thought and grasp of AI fundamentals</p>
                  </div>
                </div>
              </Card>
              <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-purple-500">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-lg font-bold text-purple-600">2</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Innovation & Creativity</h3>
                    <p className="text-gray-600">Ability to think beyond the obvious and apply ideas practically</p>
                  </div>
                </div>
              </Card>
              <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-green-500">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-lg font-bold text-green-600">3</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Analytical Skills</h3>
                    <p className="text-gray-600">Logical reasoning, data interpretation, and problem-solving approach</p>
                  </div>
                </div>
              </Card>
              <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-yellow-500">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-lg font-bold text-yellow-600">4</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Real-World Relevance</h3>
                    <p className="text-gray-600">Application of AI concepts to real-life or social challenges</p>
                  </div>
                </div>
              </Card>
              <Card className="p-6 hover:shadow-xl transition-shadow border-l-4 border-red-500">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-lg font-bold text-red-600">5</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Future Readiness</h3>
                    <p className="text-gray-600">Demonstration of curiosity, learning attitude, and awareness of emerging technologies</p>
                  </div>
                </div>
              </Card>
            </div>

            {/* CTA after Judging Criteria */}
            <div className="mt-16 text-center">
              <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8 border-2 border-indigo-200">
                <p className="text-2xl font-bold text-gray-900 mb-4">
                  Ready to be judged by the best and win big?
                </p>
                <p className="text-gray-600 mb-6 text-lg">Show your AI skills and compete with India's brightest minds</p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button 
                    size="lg" 
                    onClick={() => setStudentDialogOpen(true)}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-lg px-8"
                  >
                    <User className="w-5 h-5 mr-2" />
                    Register as Student
                  </Button>
                  <Button 
                    size="lg" 
                    onClick={() => setSchoolDialogOpen(true)}
                    variant="outline"
                    className="border-2 border-indigo-600 text-indigo-600 hover:bg-indigo-600 hover:text-white font-bold text-lg px-8"
                  >
                    <Building2 className="w-5 h-5 mr-2" />
                    Register as School
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Mentor Profiles Section */}
      <section className="py-20 bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-4">🎯 Get Mentored by the top Relevant 1%</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Connect with over <strong>100+ mentors</strong> from leading industries, providing real-world insights and hands-on career development.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Piyush Gupta</h3>
              <p className="text-sm text-gray-600">Co Founder Stride Ahead, Verismart.AI</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Himanshu Gupta</h3>
              <p className="text-sm text-gray-600">QA Manager, Aspire</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Sneha Verma</h3>
              <p className="text-sm text-gray-600">Certified Career Coach</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Saveera Bahl</h3>
              <p className="text-sm text-gray-600">Founder Director of Manasvi Wellbeing P.Ltd</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Nilay Pandey</h3>
              <p className="text-sm text-gray-600">Founder & CEO, Agrix</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Cdr. Jagmohan</h3>
              <p className="text-sm text-gray-600">Ex Indian Navy Ex-director, Quality council of India</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Manoj Sethi</h3>
              <p className="text-sm text-gray-600">Brand you coach, CEO GILP</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Dhairya Gangwani</h3>
              <p className="text-sm text-gray-600">Career Coach</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Abhinav Mahadevan</h3>
              <p className="text-sm text-gray-600">Agile Coach - Telstra</p>
            </Card>

            <Card className="p-6 text-center hover:shadow-xl transition-shadow">
              <div className="w-24 h-24 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="font-bold text-lg mb-1">Mary Tressa Gabriel</h3>
              <p className="text-sm text-gray-600">Project manager at dell</p>
            </Card>
          </div>

          {/* CTA after Mentor Profiles */}
          <div className="mt-16 text-center">
            <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-2xl p-8 border-2 border-green-200">
              <p className="text-2xl font-bold text-gray-900 mb-4">
                🎯 Get mentored by 100+ industry experts!
              </p>
              <p className="text-gray-600 mb-6 text-lg">Register now and unlock access to personalized mentorship sessions</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  size="lg" 
                  onClick={() => setStudentDialogOpen(true)}
                  className="bg-green-600 hover:bg-green-700 text-white font-bold text-lg px-8"
                >
                  <User className="w-5 h-5 mr-2" />
                  Register as Student
                </Button>
                <Button 
                  size="lg" 
                  onClick={() => setSchoolDialogOpen(true)}
                  variant="outline"
                  className="border-2 border-green-600 text-green-600 hover:bg-green-600 hover:text-white font-bold text-lg px-8"
                >
                  <Building2 className="w-5 h-5 mr-2" />
                  Register as School
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Backed By & Featured In Section */}
      <section className="py-20 bg-gray-50">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-4">We are Backed By & Featured In</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 max-w-5xl mx-auto">
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">Uincept</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">AWS Activate</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">AWS</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">Startup City</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">TechCircle</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">Economic Times</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">Your Story</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">TECHI 3D</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">Microsoft Founders Hub</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">Ed-Tech Review</p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-md flex items-center justify-center h-32">
              <div className="text-center">
                <Building2 className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-xs text-gray-500">APAC</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="container py-20">
        <h2 className="text-4xl lg:text-5xl font-bold text-center mb-16">Frequently Asked Questions</h2>
        <div className="max-w-3xl mx-auto">
          <Accordion type="single" collapsible className="space-y-4">
            <AccordionItem value="item-1" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                Who can participate in the AI Olympiad?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                The AI Olympiad is open to all high school students currently enrolled in Grades 9, 10, 11, or 12 across India. No prior coding or AI experience is required—just curiosity and enthusiasm for learning about artificial intelligence!
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-2" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                What is the registration fee?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                The registration fee is ₹99 per student. However, you can use the coupon code <strong>KEEPSTRIDING</strong> to get 100% off and register completely free! Schools registering 10 or more students also get free registration for all participants.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-3" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                What is the format and duration of the assessment?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                The assessment is a 90-minute online test consisting of multiple-choice questions, scenario-based problems, and short answer questions covering AI fundamentals, machine learning concepts, ethical considerations, and real-world applications. The test will be conducted on our secure online platform.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-4" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                Do I need coding knowledge to participate?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                No! While basic programming knowledge can be helpful, it's not mandatory. The Olympiad focuses on AI concepts, logical thinking, problem-solving, and understanding of AI applications rather than coding skills. We provide free study materials to help you prepare.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-5" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                When and how will results be announced?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                Results will be announced on 28th February 2025. All participants will receive their scores and performance reports via email. Winners will be announced on our website and social media channels. Top performers will be contacted directly for prize distribution and certificate delivery.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-6" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                What study materials are provided?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                All registered participants get free access to comprehensive study materials including AI fundamentals guide, sample questions, video tutorials, recommended reading list, and practice assessments. These resources are designed to help students from all backgrounds prepare effectively.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-7" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                Can schools register multiple students?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                Absolutely! Schools can register multiple students at once. Schools registering 10 or more students get free registration for all participants plus a unique school code, dedicated support, and recognition on our platform. Contact us for bulk registration assistance.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-8" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                What happens if I face technical issues during the assessment?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                Our technical support team will be available throughout the assessment period. If you face any issues, you can immediately contact our support via WhatsApp, email, or phone. We have backup systems and provisions for rescheduling in case of genuine technical difficulties.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-9" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                Are the certificates recognized?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                Yes! Certificates are digitally signed and recognized by leading educational institutions. Top performers also receive recommendation letters that can strengthen college applications. Many universities value participation in national-level competitions like the AI Olympiad.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-10" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                Can I get a refund if I can't participate?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                Refund requests are accepted up to 7 days before the assessment date. Please contact our support team with your registration details. However, if you used the KEEPSTRIDING coupon code for free registration, no refund processing is needed.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-11" className="border rounded-lg px-6">
              <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                How can I contact support for more questions?
              </AccordionTrigger>
              <AccordionContent className="text-gray-600 leading-relaxed">
                You can reach us via email at support@strideahead.in, call us at +91 123 456 7890, or WhatsApp us for quick responses. Our support team is available Monday to Saturday, 9 AM to 6 PM IST. You can also check our detailed FAQ section on the website.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </section>

      {/* Stride Ecosystem Section */}
      <section className="py-20 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
            backgroundSize: '50px 50px'
          }}></div>
        </div>

        <div className="relative container">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-4">
              Welcome to the Stride Ahead Ecosystem
            </h2>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto">
              The AI Olympiad is just the beginning. Join Stride Ahead and unlock a world of opportunities!
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
            {[
              { icon: BookOpen, title: "Learning Platform", desc: "Access thousands of courses, tutorials, and resources on AI, ML, and emerging technologies" },
              { icon: Users, title: "Community", desc: "Join a vibrant community of 50,000+ students, mentors, and professionals" },
              { icon: Briefcase, title: "Career Opportunities", desc: "Get access to internships, job opportunities, and career guidance from industry experts" },
              { icon: TrendingUp, title: "Skill Development", desc: "Build in-demand skills with hands-on projects, assessments, and personalized learning paths" }
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-sm rounded-xl p-6 hover:bg-white/20 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-blue-100 text-sm leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 md:p-12 text-center">
            <h3 className="text-3xl font-bold mb-4">
              Join 50,000+ Students Already Learning with Stride Ahead
            </h3>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Get free access to our learning platform, connect with mentors, and accelerate your career in tech
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-white text-blue-700 hover:bg-blue-50 text-lg px-8">
                Explore Stride Ahead
              </Button>
              <Button size="lg" variant="outline" className="border-2 border-white text-white hover:bg-white/10 text-lg px-8">
                Join Community
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Sticky Bottom CTA Strip */}
      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-2xl z-50 border-t-4 border-yellow-400">
        <div className="container py-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="text-center sm:text-left">
              <p className="font-bold text-lg">Ready to Join India's Premier AI Competition?</p>
              <p className="text-sm text-blue-100">Register now and use code KEEPSTRIDING for FREE entry!</p>
            </div>
            <div className="flex gap-3">
              <Button 
                size="lg" 
                onClick={() => setStudentDialogOpen(true)}
                className="bg-white text-blue-700 hover:bg-blue-50 font-bold shadow-lg hover:shadow-xl transition-all"
              >
                <User className="w-5 h-5 mr-2" />
                Register as Student
              </Button>
              <Button 
                size="lg" 
                onClick={() => setSchoolDialogOpen(true)}
                variant="outline"
                className="border-2 border-white text-white hover:bg-white hover:text-blue-700 font-bold shadow-lg hover:shadow-xl transition-all"
              >
                <Building2 className="w-5 h-5 mr-2" />
                Register as School
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-8 mb-24">
        <div className="container text-center">
          <p className="text-sm">
            Powered by <a href="https://strideahead.in" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 font-semibold">Stride Ahead</a>
          </p>
        </div>
      </footer>

      {/* Registration Modal */}
      <Dialog open={studentDialogOpen || schoolDialogOpen} onOpenChange={(open) => {
        if (!open) {
          setStudentDialogOpen(false);
          setSchoolDialogOpen(false);
        }
      }}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Register for AI Olympiad 2025</DialogTitle>
          </DialogHeader>

          <Tabs defaultValue={studentDialogOpen ? "student" : "school"} onValueChange={(value) => {
            setStudentDialogOpen(value === "student");
            setSchoolDialogOpen(value === "school");
          }}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="student">
                <User className="w-4 h-4 mr-2" />
                Student
              </TabsTrigger>
              <TabsTrigger value="school">
                <Building2 className="w-4 h-4 mr-2" />
                School
              </TabsTrigger>
            </TabsList>

            <TabsContent value="student">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <p className="text-sm text-blue-800">
                  <strong>Registration Fee: ₹99</strong> | Use code <strong>KEEPSTRIDING</strong> for 100% discount!
                </p>
              </div>

              <form onSubmit={handleStudentSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="firstName">First Name *</Label>
                    <Input id="firstName" name="firstName" required />
                  </div>
                  <div>
                    <Label htmlFor="lastName">Last Name *</Label>
                    <Input id="lastName" name="lastName" required />
                  </div>
                </div>
                <div>
                  <Label htmlFor="email">Email *</Label>
                  <Input id="email" name="email" type="email" required />
                </div>
                <div>
                  <Label htmlFor="mobile">Mobile Number *</Label>
                  <Input id="mobile" name="mobile" type="tel" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="grade">Grade *</Label>
                    <Select name="grade" required>
                      <SelectTrigger>
                        <SelectValue placeholder="Select grade" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="9">Grade 9</SelectItem>
                        <SelectItem value="10">Grade 10</SelectItem>
                        <SelectItem value="11">Grade 11</SelectItem>
                        <SelectItem value="12">Grade 12</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="age">Age *</Label>
                    <Input id="age" name="age" type="number" min="13" max="20" required />
                  </div>
                </div>
                <div>
                  <Label htmlFor="stream">Stream (Optional)</Label>
                  <Select name="stream">
                    <SelectTrigger>
                      <SelectValue placeholder="Select stream" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="science-pcm">Science PCM</SelectItem>
                      <SelectItem value="science-pcb">Science PCB</SelectItem>
                      <SelectItem value="commerce-with-maths">Commerce with Maths</SelectItem>
                      <SelectItem value="commerce-without-maths">Commerce without Maths</SelectItem>
                      <SelectItem value="humanities-with-maths">Humanities with Maths</SelectItem>
                      <SelectItem value="humanities-without-maths">Humanities without Maths</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="schoolName">School Name *</Label>
                  <Input id="schoolName" name="schoolName" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="city">City *</Label>
                    <Input id="city" name="city" required />
                  </div>
                  <div>
                    <Label htmlFor="state">State *</Label>
                    <Input id="state" name="state" required />
                  </div>
                </div>
                
                {/* Parental Consent Section for Minors */}
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 space-y-3">
                  <h4 className="font-semibold text-sm text-yellow-900">Parental Consent (Required for students under 18)</h4>
                  <div>
                    <Label htmlFor="parentName">Parent/Guardian Name *</Label>
                    <Input id="parentName" name="parentName" required />
                  </div>
                  <div>
                    <Label htmlFor="parentEmail">Parent/Guardian Email *</Label>
                    <Input id="parentEmail" name="parentEmail" type="email" required />
                  </div>
                  <div>
                    <Label htmlFor="parentMobile">Parent/Guardian Mobile *</Label>
                    <Input id="parentMobile" name="parentMobile" type="tel" required />
                  </div>
                </div>

                {/* Legal Consent Checkboxes */}
                <div className="space-y-3 border-t pt-4">
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="termsConsent" 
                      name="termsConsent" 
                      required 
                      className="mt-1"
                    />
                    <Label htmlFor="termsConsent" className="text-sm leading-relaxed cursor-pointer">
                      I have read and agree to the{" "}
                      <a href="/terms" target="_blank" className="text-indigo-600 hover:underline font-semibold">
                        Terms and Conditions
                      </a>
                      {" "}*
                    </Label>
                  </div>
                  
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="privacyConsent" 
                      name="privacyConsent" 
                      required 
                      className="mt-1"
                    />
                    <Label htmlFor="privacyConsent" className="text-sm leading-relaxed cursor-pointer">
                      I have read and agree to the{" "}
                      <a href="/privacy" target="_blank" className="text-indigo-600 hover:underline font-semibold">
                        Privacy Policy
                      </a>
                      {" "}*
                    </Label>
                  </div>
                  
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="parentalConsent" 
                      name="parentalConsent" 
                      required 
                      className="mt-1"
                    />
                    <Label htmlFor="parentalConsent" className="text-sm leading-relaxed cursor-pointer">
                      As a parent/guardian, I consent to my child's participation in this event and the collection and processing of their personal information as described in the Privacy Policy. *
                    </Label>
                  </div>
                  
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="dataProcessingConsent" 
                      name="dataProcessingConsent" 
                      required 
                      className="mt-1"
                    />
                    <Label htmlFor="dataProcessingConsent" className="text-sm leading-relaxed cursor-pointer">
                      I consent to the processing of my personal data for event management, communication, and related purposes. *
                    </Label>
                  </div>
                  
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="marketingConsent" 
                      name="marketingConsent" 
                      className="mt-1"
                    />
                    <Label htmlFor="marketingConsent" className="text-sm leading-relaxed cursor-pointer">
                      I would like to receive updates about future events and programs (optional)
                    </Label>
                  </div>
                </div>

                <Button type="submit" className="w-full" disabled={registerStudentMutation.isPending}>
                  {registerStudentMutation.isPending ? <Loader2 className="animate-spin" /> : "Submit Registration"}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="school">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                <p className="text-sm text-green-800">
                  <strong>School Registration is FREE!</strong> Register your school and get a unique code for your students.
                </p>
              </div>

              <form onSubmit={handleSchoolSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="schoolName">School Name *</Label>
                  <Input id="schoolName" name="schoolName" required />
                </div>
                <div>
                  <Label htmlFor="contactPerson">Principal/Coordinator Name *</Label>
                  <Input id="contactPerson" name="contactPerson" required />
                </div>
                <div>
                  <Label htmlFor="contactEmail">Email *</Label>
                  <Input id="contactEmail" name="contactEmail" type="email" required />
                </div>
                <div>
                  <Label htmlFor="contactMobile">Contact Number *</Label>
                  <Input id="contactMobile" name="contactMobile" type="tel" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="city">City *</Label>
                    <Input id="city" name="city" required />
                  </div>
                  <div>
                    <Label htmlFor="state">State *</Label>
                    <Input id="state" name="state" required />
                  </div>
                </div>
                
                {/* Legal Consent Checkboxes for Schools */}
                <div className="space-y-3 border-t pt-4">
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="schoolTermsConsent" 
                      name="termsConsent" 
                      required 
                      className="mt-1"
                    />
                    <Label htmlFor="schoolTermsConsent" className="text-sm leading-relaxed cursor-pointer">
                      I have read and agree to the{" "}
                      <a href="/terms" target="_blank" className="text-indigo-600 hover:underline font-semibold">
                        Terms and Conditions
                      </a>
                      {" "}*
                    </Label>
                  </div>
                  
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="schoolPrivacyConsent" 
                      name="privacyConsent" 
                      required 
                      className="mt-1"
                    />
                    <Label htmlFor="schoolPrivacyConsent" className="text-sm leading-relaxed cursor-pointer">
                      I have read and agree to the{" "}
                      <a href="/privacy" target="_blank" className="text-indigo-600 hover:underline font-semibold">
                        Privacy Policy
                      </a>
                      {" "}*
                    </Label>
                  </div>
                  
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="schoolDataProcessingConsent" 
                      name="dataProcessingConsent" 
                      required 
                      className="mt-1"
                    />
                    <Label htmlFor="schoolDataProcessingConsent" className="text-sm leading-relaxed cursor-pointer">
                      I consent to the processing of school and contact person data for event management and communication purposes. *
                    </Label>
                  </div>
                  
                  <div className="flex items-start space-x-2">
                    <input 
                      type="checkbox" 
                      id="schoolMarketingConsent" 
                      name="marketingConsent" 
                      className="mt-1"
                    />
                    <Label htmlFor="schoolMarketingConsent" className="text-sm leading-relaxed cursor-pointer">
                      I would like to receive updates about future events and programs (optional)
                    </Label>
                  </div>
                </div>

                <Button type="submit" className="w-full" disabled={registerSchoolMutation.isPending}>
                  {registerSchoolMutation.isPending ? <Loader2 className="animate-spin" /> : "Register School (Free)"}
                </Button>
              </form>
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </div>
  );
}
