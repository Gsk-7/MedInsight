import React, { useState } from 'react';
import { ArrowLeft, Camera, Edit2, Save, X } from 'lucide-react';
import type { User } from './types';

const mockUser: User = {
  id: '1',
  name: 'John Doe',
  email: 'john.doe@example.com',
  avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&h=150',
  role: 'Patient',
  personalInfo: {
    dateOfBirth: '1990-01-01',
    age: 33,
    gender: 'Male',
    bloodType: 'O+',
  },
  contactInfo: {
    phone: '+1 234 567 8900',
    address: '123 Medical Center St, Healthcare City',
    emergencyContact: '+1 234 567 8901',
  },
};

const App = () => {
  const [user, setUser] = useState<User>(mockUser);
  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState<User>(user);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const newAvatar = reader.result as string;
        setEditedUser(prev => ({ ...prev, avatar: newAvatar }));
        if (!isEditing) {
          setUser(prev => ({ ...prev, avatar: newAvatar }));
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (
    section: 'personalInfo' | 'contactInfo',
    field: string,
    value: string | number
  ) => {
    setEditedUser(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value,
      },
    }));
  };

  const handleSave = () => {
    setUser(editedUser);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedUser(user);
    setIsEditing(false);
  };

  const displayUser = isEditing ? editedUser : user;
  

  return (
    <div className="fixed inset-0 w-full h-full bg-white z-50 overflow-y-auto">
      {/* Back to Home Button */}
      <button
  onClick={() => {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = "/"; // Redirect to home if no history
    }
  }}
  className="absolute top-4 left-4 flex items-center px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-transform transform hover:scale-105 shadow-md"
>
  <ArrowLeft className="w-5 h-5 mr-2" />
  Back to Home
</button>
      <div className="min-h-full bg-gradient-to-br from-blue-50 to-indigo-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden transform transition-all">  
            {/* Header with User Profile Display */}
            <div className="relative bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-600 p-12">
              <div className="flex flex-col sm:flex-row items-center">
                <div className="relative group">
                  <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-white shadow-xl transition-transform duration-300 transform group-hover:scale-105">
                    <img
                      src={displayUser.avatar}
                      alt={displayUser.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <label className="absolute bottom-0 right-0 bg-blue-600 p-3 rounded-full cursor-pointer hover:bg-blue-700 transition-colors shadow-lg transform hover:scale-105">
                    <Camera className="w-5 h-5 text-white" />
                    <input
                      type="file"
                      className="hidden"
                      accept="image/*"
                      onChange={handleImageUpload}
                    />
                  </label>
                </div>
                <div className="mt-6 sm:mt-0 sm:ml-8 text-center sm:text-left">
                  <h1 className="text-3xl font-bold text-white mb-2">{displayUser.name}</h1>
                  <p className="text-blue-100 text-lg mb-3">{displayUser.email}</p>
                  <span className="inline-block px-4 py-2 bg-blue-500 bg-opacity-40 backdrop-blur-sm rounded-full text-white text-sm font-semibold">
                    {displayUser.role}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Profile Content */}
          <div className="p-8 lg:p-12">
            <div className="flex justify-end mb-8">
              {isEditing ? (
                <>
                  <button
                    onClick={handleCancel}
                    className="flex items-center px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors mr-4 transform hover:scale-105"
                  >
                    <X className="w-5 h-5 mr-2" />
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    className="flex items-center px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-colors transform hover:scale-105"
                  >
                    <Save className="w-5 h-5 mr-2" />
                    Save Changes
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex items-center px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors transform hover:scale-105"
                >
                  <Edit2 className="w-5 h-5 mr-2" />
                  Edit Profile
                </button>
              )}
            </div>

            {/* Personal Information */}
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Personal Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">Date of Birth</label>
                  <input
                    type="date"
                    value={displayUser.personalInfo.dateOfBirth}
                    onChange={(e) => handleInputChange('personalInfo', 'dateOfBirth', e.target.value)}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors disabled:bg-gray-50"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">Age</label>
                  <input
                    type="number"
                    value={displayUser.personalInfo.age}
                    onChange={(e) => handleInputChange('personalInfo', 'age', parseInt(e.target.value))}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors disabled:bg-gray-50"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">Gender</label>
                  <input
                    type="text"
                    value={displayUser.personalInfo.gender}
                    onChange={(e) => handleInputChange('personalInfo', 'gender', e.target.value)}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors disabled:bg-gray-50"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">Blood Type</label>
                  <input
                    type="text"
                    value={displayUser.personalInfo.bloodType}
                    onChange={(e) => handleInputChange('personalInfo', 'bloodType', e.target.value)}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors disabled:bg-gray-50"
                  />
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Contact Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">Phone</label>
                  <input
                    type="tel"
                    value={displayUser.contactInfo.phone}
                    onChange={(e) => handleInputChange('contactInfo', 'phone', e.target.value)}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors disabled:bg-gray-50"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">Emergency Contact</label>
                  <input
                    type="tel"
                    value={displayUser.contactInfo.emergencyContact}
                    onChange={(e) => handleInputChange('contactInfo', 'emergencyContact', e.target.value)}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors disabled:bg-gray-50"
                  />
                </div>
                <div className="col-span-2 space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">Address</label>
                  <textarea
                    value={displayUser.contactInfo.address}
                    onChange={(e) => handleInputChange('contactInfo', 'address', e.target.value)}
                    disabled={!isEditing}
                    rows={3}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors disabled:bg-gray-50 resize-none"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
