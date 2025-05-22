import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import FileUpload from './components/FileUpload';
import MovieDetails from './components/MovieDetails';
import RecentDetections from './components/RecentDetections';
import Footer from './components/Footer';
import { ThemeProvider } from './context/ThemeContext';
import { sampleMovies } from './utils/sampleData';

function App() {
  const [detectedMovie, setDetectedMovie] = useState<any>(null);
  const [recentMovies, setRecentMovies] = useState<any[]>(sampleMovies.slice(0, 3));

  const handleMovieDetected = (movieData: any) => {
    setDetectedMovie(movieData);
    
    // Add to recently detected if not already there
    if (!recentMovies.some(movie => movie.id === movieData.id)) {
      setRecentMovies(prev => [movieData, ...prev].slice(0, 5));
    }
  };

  const closeMovieDetails = () => {
    setDetectedMovie(null);
  };

  const handleViewDetails = (movie: any) => {
    setDetectedMovie(movie);
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-slate-900 text-slate-900 dark:text-white transition-colors duration-300">
        <Header />
        <main>
          <Hero />
          <FileUpload onMovieDetected={handleMovieDetected} />
          <RecentDetections 
            movies={recentMovies} 
            onViewDetails={handleViewDetails} 
          />
        </main>
        <Footer />
        
        {detectedMovie && (
          <MovieDetails movie={detectedMovie} onClose={closeMovieDetails} />
        )}
      </div>
    </ThemeProvider>
  );
}

export default App;