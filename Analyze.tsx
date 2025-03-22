import React, { useState } from 'react';
import { Activity, Calendar as CalendarIcon, Clock, FileText, Heart, User, ChevronDown, AlertTriangle, CheckCircle, Phone, Mail, MapPin, Star, ArrowLeft, Search, Filter } from 'lucide-react';
import { format, addDays, isSameDay } from 'date-fns';
import { useNavigate } from 'react-router-dom';

// Add detailed summary to the medical report data
const medicalReport = {
  patientName: "John Doe",
  age: 35,
  date: "2024-03-15",
  detailedSummary: `Based on your recent medical analysis, we've identified some cardiovascular health concerns that require attention. Your test results show slightly elevated cholesterol levels and mild hypertension, which, while not immediately critical, suggest the need for lifestyle modifications and preventive care.

The combination of occasional chest discomfort and shortness of breath during exercise, along with your family history of heart disease, indicates that these symptoms should be monitored closely. However, it's important to note that your overall health status is stable, and these conditions are manageable with appropriate lifestyle changes and medical supervision.

We strongly recommend following the suggested precautions, particularly focusing on regular cardiovascular exercise and dietary modifications. Additionally, consultation with a cardiologist would be beneficial for developing a comprehensive management plan. The good news is that early detection allows us to address these concerns proactively, significantly improving long-term health outcomes.`,
  summary: {
    classification: "Attention Needed",
    mainIssues: ["Elevated cholesterol", "Mild hypertension"],
    symptoms: [
      "Occasional chest discomfort",
      "Shortness of breath during exercise",
      "Fatigue"
    ],
    causes: [
      "Sedentary lifestyle",
      "High-fat diet",
      "Family history of heart disease"
    ],
    precautions: [
      "Regular cardiovascular exercise",
      "Low-sodium, low-fat diet",
      "Regular blood pressure monitoring",
      "Stress management"
    ],
    recommendedSpecialists: ["Cardiologist", "Nutritionist"]
  },
  vitals: {
    heartRate: "72 bpm",
    bloodPressure: "120/80 mmHg",
    temperature: "98.6°F",
    oxygenSaturation: "98%"
  },
  analysis: [
    {
      category: "Blood Work",
      status: "Normal",
      details: "All blood parameters are within normal range",
      recommendations: "Continue regular health maintenance"
    },
    {
      category: "Cardiac Function",
      status: "Attention Needed",
      details: "Slight elevation in cholesterol levels",
      recommendations: "Dietary modifications recommended"
    },
    {
      category: "Respiratory",
      status: "Normal",
      details: "Normal respiratory function",
      recommendations: "No specific action needed"
    }
  ]
};

// Extended mock doctors data with more specialties
const allDoctors = [
  {
    id: 1,
    name: "Dr. Sarah Johnson",
    specialty: "Cardiologist",
    experience: "15 years",
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Downtown Medical Center",
    education: "Harvard Medical School",
    contact: {
      phone: "+1 (555) 123-4567",
      email: "dr.johnson@medical.com"
    }
  },
  {
    id: 2,
    name: "Dr. Michael Chen",
    specialty: "Cardiologist",
    experience: "12 years",
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Heart Care Specialists",
    education: "Stanford Medical School",
    contact: {
      phone: "+1 (555) 234-5678",
      email: "dr.chen@medical.com"
    }
  },
  {
    id: 3,
    name: "Dr. Emily Rodriguez",
    specialty: "Nutritionist",
    experience: "8 years",
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1594824476967-48c8b964273f?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Wellness Nutrition Center",
    education: "Yale School of Medicine",
    contact: {
      phone: "+1 (555) 345-6789",
      email: "dr.rodriguez@medical.com"
    }
  },
  {
    id: 4,
    name: "Dr. James Wilson",
    specialty: "Dentist",
    experience: "20 years",
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Smile Perfect Dental",
    education: "University of Pennsylvania",
    contact: {
      phone: "+1 (555) 456-7890",
      email: "dr.wilson@medical.com"
    }
  },
  {
    id: 5,
    name: "Dr. Lisa Thompson",
    specialty: "Gynecologist",
    experience: "18 years",
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1527613426441-4da17471b66d?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Women's Health Center",
    education: "Johns Hopkins University",
    contact: {
      phone: "+1 (555) 567-8901",
      email: "dr.thompson@medical.com"
    }
  },
  {
    id: 6,
    name: "Dr. Robert Kim",
    specialty: "Pediatrician",
    experience: "14 years",
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Children's Medical Group",
    education: "Columbia University",
    contact: {
      phone: "+1 (555) 678-9012",
      email: "dr.kim@medical.com"
    }
  },
  {
    id: 7,
    name: "Dr. Maria Garcia",
    specialty: "Dermatologist",
    experience: "16 years",
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1591604021695-0c69b7c05981?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Skin Care Clinic",
    education: "UCLA Medical School",
    contact: {
      phone: "+1 (555) 789-0123",
      email: "dr.garcia@medical.com"
    }
  },
  {
    id: 8,
    name: "Dr. David Lee",
    specialty: "Orthopedist",
    experience: "22 years",
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1622902046580-2b47f47f5471?auto=format&fit=crop&q=80&w=300&h=300",
    location: "Orthopedic Specialists",
    education: "Mayo Medical School",
    contact: {
      phone: "+1 (555) 890-1234",
      email: "dr.lee@medical.com"
    }
  }
];

const specialties = [
  "All Specialists",
  "Cardiologist",
  "Nutritionist",
  "Dentist",
  "Gynecologist",
  "Pediatrician",
  "Dermatologist",
  "Orthopedist"
];

const timeSlots = [
  "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
  "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
];

function App() {
  const [showDoctorBooking, setShowDoctorBooking] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState<number | null>(null);
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState("All Specialists");
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate()

  // Generate next 7 days for the calendar
  const dates = Array.from({ length: 7 }, (_, i) => addDays(new Date(), i));

  const filteredDoctors = allDoctors.filter(doctor => {
    const matchesSpecialty = selectedSpecialty === "All Specialists" || doctor.specialty === selectedSpecialty;
    const matchesSearch = doctor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         doctor.specialty.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSpecialty && matchesSearch;
  });

  const handleAppointmentSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const doctor = allDoctors.find(d => d.id === selectedDoctor);
    alert(`Appointment requested with ${doctor?.name} for ${selectedDate} at ${selectedTime}`);
    setSelectedDoctor(null);
    setSelectedDate('');
    setSelectedTime('');
  };

  const getStatusColor = (classification: string) => {
    switch (classification.toLowerCase()) {
      case 'normal':
        return 'bg-green-100 text-green-800';
      case 'attention needed':
        return 'bg-yellow-100 text-yellow-800';
      case 'consult doctor':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (showDoctorBooking) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        <header className="bg-white shadow-sm mb-6">
          <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <button
                  onClick={() => setShowDoctorBooking(false)}
                  className="mr-4 text-gray-600 hover:text-gray-900"
                >
                  <ArrowLeft className="h-6 w-6" />
                </button>
                <h1 className="text-2xl font-bold text-gray-900">Book Appointment</h1>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Search and Filter Section */}
          <div className="mb-8">
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search doctors by name or specialty..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <div className="relative">
                <select
                  value={selectedSpecialty}
                  onChange={(e) => setSelectedSpecialty(e.target.value)}
                  className="w-full sm:w-48 pl-4 pr-10 py-2 border border-gray-300 rounded-lg appearance-none bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {specialties.map(specialty => (
                    <option key={specialty} value={specialty}>{specialty}</option>
                  ))}
                </select>
                <Filter className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5 pointer-events-none" />
              </div>
            </div>
          </div>

          {/* Doctors List */}
          <div className="space-y-6">
            {filteredDoctors.map((doctor) => (
              <div key={doctor.id} className="bg-white rounded-lg shadow-sm overflow-hidden">
                <div className="p-6">
                  <div className="flex items-start">
                    <img
                      src={doctor.image}
                      alt={doctor.name}
                      className="w-24 h-24 rounded-lg object-cover mr-6"
                    />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-xl font-semibold">{doctor.name}</h3>
                          <p className="text-blue-600">{doctor.specialty}</p>
                        </div>
                        <div className="flex items-center">
                          <Star className="h-5 w-5 text-yellow-400 fill-current" />
                          <span className="ml-1 text-gray-600">{doctor.rating}</span>
                        </div>
                      </div>
                      
                      <div className="mt-2 grid grid-cols-2 gap-4">
                        <div className="flex items-center text-gray-600">
                          <MapPin className="h-4 w-4 mr-2" />
                          {doctor.location}
                        </div>
                        <div className="flex items-center text-gray-600">
                          <Clock className="h-4 w-4 mr-2" />
                          {doctor.experience} experience
                        </div>
                      </div>

                      {selectedDoctor === doctor.id ? (
                        <form onSubmit={handleAppointmentSubmit} className="mt-4">
                          {/* Calendar View */}
                          <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Select Date
                            </label>
                            <div className="grid grid-cols-7 gap-2">
                              {dates.map((date) => (
                                <button
                                  key={date.toISOString()}
                                  type="button"
                                  onClick={() => setSelectedDate(format(date, 'yyyy-MM-dd'))}
                                  className={`p-2 text-center rounded-lg transition-colors ${
                                    selectedDate === format(date, 'yyyy-MM-dd')
                                      ? 'bg-blue-600 text-white'
                                      : 'bg-gray-50 hover:bg-gray-100'
                                  }`}
                                >
                                  <div className="text-xs mb-1">{format(date, 'EEE')}</div>
                                  <div className="font-semibold">{format(date, 'd')}</div>
                                </button>
                              ))}
                            </div>
                          </div>

                          {/* Time Slots */}
                          {selectedDate && (
                            <div className="mb-4">
                              <label className="block text-sm font-medium text-gray-700 mb-2">
                                Select Time
                              </label>
                              <div className="grid grid-cols-4 sm:grid-cols-6 gap-2">
                                {timeSlots.map((time) => (
                                  <button
                                    key={time}
                                    type="button"
                                    onClick={() => setSelectedTime(time)}
                                    className={`p-2 text-center rounded-lg transition-colors ${
                                      selectedTime === time
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-gray-50 hover:bg-gray-100'
                                    }`}
                                  >
                                    {time}
                                  </button>
                                ))}
                              </div>
                            </div>
                          )}

                          <div className="flex space-x-4">
                            <button
                              type="submit"
                              disabled={!selectedDate || !selectedTime}
                              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              Confirm Booking
                            </button>
                            <button
                              type="button"
                              onClick={() => setSelectedDoctor(null)}
                              className="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                            >
                              Cancel
                            </button>
                          </div>
                        </form>
                      ) : (
                        <button
                          onClick={() => setSelectedDoctor(doctor.id)}
                          className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                        >
                          Book Appointment
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
            <button
                onClick={() => navigate('/')} // Navigate to the home page
                className="mr-4 text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="h-6 w-6" />
              </button>
              <Activity className="h-8 w-8 text-blue-600" />
              <h1 className="ml-2 text-2xl font-bold text-gray-900">Medical Analysis Report</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                Report Date: {medicalReport.date}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Summary Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <AlertTriangle className="h-5 w-5 text-blue-600 mr-2" />
              <h2 className="text-xl font-semibold">Analysis Summary</h2>
            </div>
            <span className={`px-4 py-1 rounded-full text-sm font-medium ${getStatusColor(medicalReport.summary.classification)}`}>
              {medicalReport.summary.classification}
            </span>
          </div>

          {/* Detailed Summary */}
          <div className="mb-6">
            <div className="prose max-w-none">
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {medicalReport.detailedSummary}
              </p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Main Issues</h3>
              <ul className="list-disc list-inside text-gray-600 space-y-1">
                {medicalReport.summary.mainIssues.map((issue, index) => (
                  <li key={index}>{issue}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Symptoms</h3>
              <ul className="list-disc list-inside text-gray-600 space-y-1">
                {medicalReport.summary.symptoms.map((symptom, index) => (
                  <li key={index}>{symptom}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Possible Causes</h3>
              <ul className="list-disc list-inside text-gray-600 space-y-1">
                {medicalReport.summary.causes.map((cause, index) => (
                  <li key={index}>{cause}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Recommended Precautions</h3>
              <ul className="list-disc list-inside text-gray-600 space-y-1">
                {medicalReport.summary.precautions.map((precaution, index) => (
                  <li key={index}>{precaution}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <button
              onClick={() => setShowDoctorBooking(true)}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center justify-center"
            >
              Book Appointment with Specialist
              <ArrowLeft className="h-5 w-5 ml-2 transform rotate-180" />
            </button>
          </div>
        </div>

        {/* Patient Information */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center mb-4">
            <User className="h-5 w-5 text-blue-600 mr-2" />
            <h2 className="text-xl font-semibold">Patient Information</h2>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-600">Name: {medicalReport.patientName}</p>
              <p className="text-gray-600">Age: {medicalReport.age}</p>
            </div>
            <div>
              <p className="text-gray-600">Date: {medicalReport.date}</p>
            </div>
          </div>
        </div>

        {/* Vitals */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center mb-4">
            <Heart className="h-5 w-5 text-blue-600 mr-2" />
            <h2 className="text-xl font-semibold">Vital Signs</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {Object.entries(medicalReport.vitals).map(([key, value]) => (
              <div key={key} className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500 capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</p>
                <p className="text-lg font-semibold text-gray-900">{value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Analysis Results */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center mb-4">
            <FileText className="h-5 w-5 text-blue-600 mr-2" />
            <h2 className="text-xl font-semibold">Analysis Results</h2>
          </div>
          <div className="space-y-4">
            {medicalReport.analysis.map((item, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-medium">{item.category}</h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    item.status === 'Normal' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {item.status}
                  </span>
                </div>
                <p className="text-gray-600 mb-2">{item.details}</p>
                <p className="text-sm text-gray-500">
                  <strong>Recommendation:</strong> {item.recommendations}
                </p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
