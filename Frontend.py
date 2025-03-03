import React, { useState, useEffect, useMemo } from 'react';
import {
  Bell, Bot, X, FileUp, Settings, HelpCircle, History,
  User, Sun, Moon, Brain, FileImage, FileText, Activity,
  Globe2, ChevronDown, UserCircle
} from 'lucide-react';

interface Report {
  id: string;
  name: string;
  date: string;
  status: 'Normal' | 'Alert' | 'Requires Consultation';
  type: string;
}

interface Notification {
  id: string;
  title: string;
  message: string;
  time: string;
  read: boolean;
}

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [isChatOpen, setChatOpen] = useState(false);
  const [isNotificationOpen, setNotificationOpen] = useState(false);
  const [activeUploadTab, setActiveUploadTab] = useState<'documents' | 'images'>('documents');
  const [isLanguageDropdownOpen, setLanguageDropdownOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [apiData, setApiData] = useState<any>(null);
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState<{ role: string; content: string }[]>([
    { role: "assistant", content: "Hello! I'm your medical assistant. How can I help you today?" }
  ]);

  // Define notifications and reports as state variables
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: '1',
      title: 'New Report Analysis',
      message: 'Your blood test results have been analyzed.',
      time: '2 hours ago',
      read: false
    },
    {
      id: '2',
      title: 'Appointment Reminder',
      message: 'You have an appointment with Dr. Johnson tomorrow at 10:00 AM.',
      time: '1 day ago',
      read: true
    },
    {
      id: '3',
      title: 'New Feature Available',
      message: 'Try our new AI-powered report comparison tool.',
      time: '3 days ago',
      read: true
    }
  ]);

  const [reports, setReports] = useState<Report[]>([
    {
      id: '1',
      name: 'Blood Test Results',
      date: '2024-03-15',
      status: 'Normal',
      type: 'Blood Work'
    },
    {
      id: '2',
      name: 'Cardiac Assessment',
      date: '2024-03-10',
      status: 'Alert',
      type: 'Cardiology'
    }
  ]);

  const languages = [
    'English',
    'Español',
    'Français',
    '中文',
    'العربية',
    'हिन्दी (Hindi)',
    'தமிழ் (Tamil)',
    'മലയാളം (Malayalam)',
    'বাংলা (Bengali)',
    'తెలుగు (Telugu)',
    'मराठी (Marathi)',
    'ગુજરાતી (Gujarati)',
    'ਪੰਜਾਬੀ (Punjabi)',
    'ಕನ್ನಡ (Kannada)',
    'ଓଡ଼ିଆ (Odia)',
    'অসমীয়া (Assamese)'
  ];

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Add user message to conversation
    setConversation((prev) => [...prev, { role: "user", content: message }]);

    // Clear the input
    setMessage("");

    try {
      // Send user message to backend
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response from Gemini');
      }

      const data = await response.json();

      // Add Gemini's response to conversation
      setConversation((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch (error) {
      console.error('Error:', error);
      // Fallback response if API call fails
      setConversation((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I couldn't process your request. Please try again." },
      ]);
    }
  };

  useEffect(() => {
    fetch('http://localhost:5000/api/data')
      .then(response => response.json())
      .then(data => {
        console.log("Fetched data:", data); // Log the fetched data
        setApiData(data); // Update state with fetched data
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        // Fallback to mock data if the API call fails
        setApiData({
          status: "success",
          data: {
            user: {
              id: "user123",
              name: "John Doe",
              email: "john.doe@example.com"
            },
            reports: [
              {
                id: "report1",
                title: "Blood Test Analysis",
                date: "2024-03-15",
                summary: "All values within normal range"
              },
              {
                id: "report2",
                title: "Cardiac Assessment",
                date: "2024-03-10",
                summary: "Minor irregularities detected, follow-up recommended"
              }
            ],
            recommendations: [
              "Maintain regular exercise routine",
              "Follow up with cardiologist in 3 months",
              "Continue current medication regimen"
            ]
          }
        });
      });
  }, []);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  // Calculate unread notifications count dynamically
  const unreadNotificationsCount = useMemo(() => notifications.filter(n => !n.read).length, [notifications]);

  const UploadArea = ({ type }: { type: 'documents' | 'images' }) => {
    const isDocuments = type === 'documents';
    return (
      <div className={`mt-4 border-2 border-dashed ${
        isDarkMode ? 'border-gray-600' : 'border-gray-300'
      } rounded-lg p-6`}>
        {isDocuments ? (
          <FileText className={`mx-auto h-12 w-12 ${
            isDarkMode ? 'text-gray-500' : 'text-gray-400'
          }`} />
        ) : (
          <FileImage className={`mx-auto h-12 w-12 ${
            isDarkMode ? 'text-gray-500' : 'text-gray-400'
          }`} />
        )}
        <p className={`mt-4 text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
          Drag and drop your {isDocuments ? 'medical documents' : 'medical images'} here, or{' '}
          <button className="text-indigo-500 hover:text-indigo-400 font-medium">
            browse files
          </button>
        </p>
        <p className={`mt-2 text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          Supported formats: {isDocuments ? 'PDF, XLSX, XLS, DOC, DOCX' : 'JPG, PNG, DICOM'}
        </p>
      </div>
    );
  };

  return (
    <div className={`min-h-screen flex flex-col transition-colors duration-200 ${
      isDarkMode ? 'dark bg-gray-900' : 'bg-gray-50'
    }`}>
      {/* Header */}
      <header className={`${isDarkMode ? 'bg-gray-800' : 'bg-white'} shadow-sm`}>
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Brain className={`h-8 w-8 ${isDarkMode ? 'text-indigo-400' : 'text-indigo-600'}`} />
            <h1 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
              MedInsight
            </h1>
          </div>
          <div className="flex items-center space-x-4">
             {/* Notifications */}
             <div className="relative">
              <button
                onClick={() => setNotificationOpen(!isNotificationOpen)}
                className={`p-2 rounded-lg relative ${
                  isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >
                <Bell className={`h-6 w-6 ${isDarkMode ? 'text-white' : 'text-gray-600'}`} />
                {unreadNotificationsCount > 0 && (
                  <span className="absolute top-0 right-0 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs text-white">
                    {unreadNotificationsCount}
                  </span>
                )}
              </button>
              
              {isNotificationOpen && (
                <div className={`absolute right-0 mt-2 w-80 rounded-md shadow-lg ${
                  isDarkMode ? 'bg-gray-800' : 'bg-white'
                } ring-1 ring-black ring-opacity-5 z-50`}>
                  <div className="p-4 border-b border-gray-200">
                    <h3 className={`font-medium ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                      Notifications
                    </h3>
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    {notifications.length > 0 ? (
                      notifications.map((notification) => (
                        <div 
                          key={notification.id}
                          className={`p-4 ${
                            notification.read 
                              ? '' 
                              : isDarkMode ? 'bg-gray-700' : 'bg-indigo-50'
                          } ${
                            isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                          } border-b border-gray-200`}
                        >
                          <div className="flex justify-between">
                            <h4 className={`font-medium ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                              {notification.title}
                            </h4>
                            <span className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                              {notification.time}
                            </span>
                          </div>
                          <p className={`text-sm mt-1 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                            {notification.message}
                          </p>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 text-center">
                        <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                          No notifications yet
                        </p>
                      </div>
                    )}
                  </div>
                  <div className="p-2 text-center border-t border-gray-200">
                    <button className={`text-sm ${isDarkMode ? 'text-indigo-400' : 'text-indigo-600'} hover:underline`}>
                      Mark all as read
                    </button>
                  </div>
                </div>
              )}
            </div>
            {/* Language Selector */}
            <div className="relative">
              <button
                onClick={() => setLanguageDropdownOpen(!isLanguageDropdownOpen)}
                className={`flex items-center space-x-2 p-2 rounded-lg ${
                  isDarkMode ? 'hover:bg-gray-700 text-white' : 'hover:bg-gray-100 text-gray-600'
                }`}
              >
                <Globe2 className="h-5 w-5" />
                <span>{selectedLanguage}</span>
                <ChevronDown className="h-4 w-4" />
              </button>
              {isLanguageDropdownOpen && (
                <div className={`absolute right-0 mt-2 w-48 rounded-md shadow-lg ${
                  isDarkMode ? 'bg-gray-800' : 'bg-white'
                } ring-1 ring-black ring-opacity-5 z-50`}>
                  <div className="py-1">
                    {languages.map((lang) => (
                      <button
                        key={lang}
                        onClick={() => {
                          setSelectedLanguage(lang);
                          setLanguageDropdownOpen(false);
                        }}
                        className={`block w-full text-left px-4 py-2 text-sm ${
                          isDarkMode 
                            ? 'text-gray-300 hover:bg-gray-700' 
                            : 'text-gray-700 hover:bg-gray-100'
                        }`}
                      >
                        {lang}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}
            >
              {isDarkMode ? (
                <Sun className="h-6 w-6 text-yellow-400" />
              ) : (
                <Moon className="h-6 w-6 text-gray-600" />
              )}
            </button>

            {/* Profile */}
            <button
              onClick={() => setSidebarOpen(true)}
              className={`flex items-center space-x-2 p-2 rounded-lg ${
                isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
              }`}
            >
              <UserCircle className={`h-6 w-6 ${isDarkMode ? 'text-white' : 'text-gray-600'}`} />
              <span className={isDarkMode ? 'text-white' : 'text-gray-600'}>John Doe</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow max-w-4xl mx-auto px-4 py-8">
        <div className={`${
          isDarkMode ? 'bg-gray-800' : 'bg-white'
        } rounded-lg shadow-lg p-8`}>
          <h2 className={`text-2xl font-semibold text-center ${
            isDarkMode ? 'text-white' : 'text-gray-900'
          }`}>
            Upload Medical Reports
          </h2>
          
          {/* Upload Tabs */}
          <div className="mt-6 border-b border-gray-200">
            <div className="flex space-x-8">
              <button
                onClick={() => setActiveUploadTab('documents')}
                className={`pb-4 relative ${
                  activeUploadTab === 'documents'
                    ? `${isDarkMode ? 'text-indigo-400' : 'text-indigo-600'}`
                    : `${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`
                }`}
              >
                <div className="flex items-center space-x-2">
                  <FileText className="h-5 w-5" />
                  <span>Documents</span>
                </div>
                {activeUploadTab === 'documents' && (
                  <div className={`absolute bottom-0 left-0 w-full h-0.5 ${
                    isDarkMode ? 'bg-indigo-400' : 'bg-indigo-600'
                  }`} />
                )}
              </button>
              <button
                onClick={() => setActiveUploadTab('images')}
                className={`pb-4 relative ${
                  activeUploadTab === 'images'
                    ? `${isDarkMode ? 'text-indigo-400' : 'text-indigo-600'}`
                    : `${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`
                }`}
              >
                <div className="flex items-center space-x-2">
                  <FileImage className="h-5 w-5" />
                  <span>Images</span>
                </div>
                {activeUploadTab === 'images' && (
                  <div className={`absolute bottom-0 left-0 w-full h-0.5 ${
                    isDarkMode ? 'bg-indigo-400' : 'bg-indigo-600'
                  }`} />
                )}
              </button>
            </div>
          </div>

          {/* Upload Areas */}
          <div className="mt-6">
            {activeUploadTab === 'documents' ? (
              <UploadArea type="documents" />
            ) : (
              <UploadArea type="images" />
            )}
          </div>
        </div>

        {/* Results Section */}
        {reports.length > 0 && (
          <div className={`mt-8 ${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
            <h3 className={`text-xl font-semibold mb-4 ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Analysis Results
            </h3>
            <div className="space-y-4">
              {reports.map((report) => (
                <div
                  key={report.id}
                  className={`${
                    isDarkMode ? 'bg-gray-700' : 'bg-gray-50'
                  } rounded-lg p-4 transition-shadow hover:shadow-md`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className={`font-medium ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                        {report.name}
                      </h4>
                      <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                        {report.date}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      report.status === 'Normal'
                        ? 'bg-green-100 text-green-800'
                        : report.status === 'Alert'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {report.status}
                    </span>
                  </div>
                  <button className="mt-3 flex items-center text-sm text-indigo-500 hover:text-indigo-400">
                    <Activity className="h-4 w-4 mr-1" />
                    View Detailed Analysis
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* API Data Section */}
        <div className={`mt-8 ${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
          <h3 className={`text-xl font-semibold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
            API Data
          </h3>
          {apiData ? (
            <pre className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'} overflow-auto`}>
              {JSON.stringify(apiData, null, 2)}
            </pre>
          ) : (
            <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
              Loading data...
            </p>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className={`mt-auto py-8 ${isDarkMode ? 'bg-gray-800' : 'bg-white'} shadow-inner`}>
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h4 className={`font-semibold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                About
              </h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    About Us
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Our Mission
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Team
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className={`font-semibold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                Support
              </h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Help Center
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Contact Us
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    FAQs
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className={`font-semibold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                Legal
              </h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Terms of Service
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Cookie Policy
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className={`font-semibold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                Connect
              </h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Twitter
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    LinkedIn
                  </a>
                </li>
                <li>
                  <a href="#" className={`text-sm ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    Facebook
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className={`mt-8 pt-8 border-t ${isDarkMode ? 'border-gray-700' : 'border-gray-200'} text-center`}>
            <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              © 2024 MedInsight. All rights reserved.
            </p>
          </div>
        </div>
      </footer>

      {/* Sidebar */}
      <div className={`fixed inset-y-0 right-0 w-64 ${
        isDarkMode ? 'bg-gray-800' : 'bg-white'
      } shadow-lg transform ${
        isSidebarOpen ? 'translate-x-0' : 'translate-x-full'
      } transition-transform duration-200 ease-in-out z-30`}>
        <div className="p-4">
          <div className="flex items-center justify-between mb-8">
            <h2 className={`text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
              Profile
            </h2>
            <button
              onClick={() => setSidebarOpen(false)}
              className={`p-2 rounded-lg ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}
            >
              <X className={`h-5 w-5 ${isDarkMode ? 'text-white' : 'text-gray-600'}`} />
            </button>
          </div>
          
          {/* Profile Section */}
          <div className="mb-8 text-center">
            <UserCircle className={`h-20 w-20 mx-auto ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`} />
            <h3 className={`mt-4 font-medium ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>John Doe</h3>
            <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>john.doe@example.com</p>
          </div>

          <nav className="space-y-2">
            <button className={`flex items-center space-x-3 w-full p-3 rounded-lg ${
              isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
            }`}>
              <User className={`h-5 w-5 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`} />
              <span className={`${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Account</span>
            </button>
            <button className={`flex items-center space-x-3 w-full p-3 rounded-lg ${
              isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
            }`}>
              <History className={`h-5 w-5 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`} />
              <span className={`${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>History</span>
            </button>
            <button className={`flex items-center space-x-3 w-full p-3 rounded-lg ${
              isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
            }`}>
              <Settings className={`h-5 w-5 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`} />
              <span className={`${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Settings</span>
            </button>
            <button className={`flex items-center space-x-3 w-full p-3 rounded-lg ${
              isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
            }`}>
              <HelpCircle className={`h-5 w-5 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`} />
              <span className={`${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Help</span>
            </button>
          </nav>
        </div>
      </div>

      {/* Chatbot */}
      <div className="fixed bottom-4 right-4 z-20">
        {isChatOpen ? (
          <div className={`${
            isDarkMode ? 'bg-gray-800' : 'bg-white'
          } rounded-lg shadow-lg w-80 h-96 flex flex-col`}>
            <div className={`p-4 border-b ${
              isDarkMode ? 'border-gray-700' : 'border-gray-200'
            } flex items-center justify-between`}>
              <div className="flex items-center space-x-2">
                <Bot className={`h-5 w-5 ${isDarkMode ? 'text-indigo-400' : 'text-indigo-600'}`} />
                <h3 className={`font-medium ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                  AI Assistant
                </h3>
              </div>
              <button
                onClick={() => setChatOpen(false)}
                className={`p-1 rounded-lg ${
                  isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >
                <X className={`h-5 w-5 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`} />
              </button>
            </div>
            <div className={`flex-1 p-4 overflow-y-auto ${
              isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
            }`}>
              <div className="space-y-4">
                {conversation.map((msg, index) => (
                  <div key={index} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                    <div className={`rounded-lg p-3 max-w-[80%] ${
                      msg.role === "user"
                        ? isDarkMode ? 'bg-indigo-600 text-white' : 'bg-indigo-100 text-gray-800'
                        : isDarkMode ? 'bg-gray-700 text-white' : 'bg-gray-200 text-gray-800'
                    }`}>
                      <p className="text-sm">{msg.content}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="p-4">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                  className={`flex-1 px-3 py-2 rounded-lg ${
                    isDarkMode 
                      ? 'bg-gray-700 text-white placeholder-gray-400 border-gray-600' 
                      : 'bg-gray-100 text-gray-900 placeholder-gray-500 border-gray-300'
                  } border focus:outline-none focus:ring-2 focus:ring-indigo-500`}
                  placeholder="Type your question..."
                />
                <button
                  onClick={sendMessage}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setChatOpen(true)}
            className={`p-4 rounded-full shadow-lg ${
              isDarkMode ? 'bg-indigo-600' : 'bg-indigo-600'
            } hover:bg-indigo-700 transition-colors`}
          >
            <Bot className="h-6 w-6 text-white" />
          </button>
        )}
      </div>

      {/* Overlay for sidebar */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-20"
          onClick={() => setSidebarOpen(false)}
        />
      )}

       {/* Overlay for notifications */}
       {isNotificationOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setNotificationOpen(false)}
        />
      )}
    </div>
  );
}

export default App;
