"use client"

import type React from "react"
import Image from "next/image"
import { useState } from "react"
import { Search, MapPin, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { MovieCard } from "@/components/movie-card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

const sampleMovies = [
  {
    id: 1,
    title: "Happy Together (春光乍泄)",
    genre: "Drama",
    rating: "4K Restoration",
    runtime: "Director: Wong Kar-Wai",
    theater: "Rio Theatre, 1660 E Broadway, Vancouver, BC V5N 1W1",
    showtimes: ["8/30 Sat 12:30 PM"],
    image: "/happy-together-poster.jpg",
  },
  {
    id: 2,
    title: "Vive L'Amour (爱情万岁)",
    genre: "Drama",
    rating: "Classic",
    runtime: "Director: Tsai Ming-Liang",
    theater: "Rio Theatre, 1660 E Broadway, Vancouver, BC V5N 1W1",
    showtimes: ["8/30 Sat 3:00 PM"],
    image: "/vive-lamour-poster.jpg",
  },
  {
    id: 3,
    title: "Lan Yu (蓝宇)",
    genre: "Romance",
    rating: "4K Restoration",
    runtime: "Director: Stanley Kwan",
    theater: "Rio Theatre, 1660 E Broadway, Vancouver, BC V5N 1W1",
    showtimes: ["9/7 Sun 2:45 PM"],
    image: "/lan-yu-poster.jpg",
  },
  {
    id: 4,
    title: "All Shall Be Well (从今以后)",
    genre: "Drama",
    rating: "New Release",
    runtime: "Director: Ray Yeung",
    theater: "Rio Theatre, 1660 E Broadway, Vancouver, BC V5N 1W1",
    showtimes: ["9/7 Sun 12:30 PM"],
    image: "/all-shall-be-well-poster.jpg",
  },
  {
    id: 5,
    title: "Chinatown Cha-Cha",
    genre: "Documentary",
    rating: "Q&A Event",
    runtime: "Director: Luka Yuanyuan Yang",
    theater: "Historic Admiral Theater, 2343 California Ave SW, Seattle, WA 98116",
    showtimes: ["5/18 1:30 PM"],
    image: "/chinatown-cha-cha-poster.jpg",
  },
]

export default function MovieResearchPage() {
  const [zipCode, setZipCode] = useState("")
  const [searchedZip, setSearchedZip] = useState("")
  const [movies, setMovies] = useState<typeof sampleMovies>([])
  const [selectedCity, setSelectedCity] = useState("Seattle")

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()

    // Validate US zip code (5 digits)
    const zipRegex = /^\d{5}$/
    if (!zipRegex.test(zipCode)) {
      alert("Please enter a valid 5-digit US zip code")
      return
    }

    setSearchedZip(zipCode)
    setMovies(sampleMovies)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <Image src="/start-logo.png" alt="STArt Film Studio Logo" width={56} height={56} className="h-14 w-14" />
            <h1 className="text-2xl font-bold text-foreground" style={{ fontFamily: "Myriad Pro, sans-serif" }}>
              STArt Film Studio
            </h1>
          </div>
        </div>
      </header>

      {/* Now showing section without poster images */}
      <section className="border-b border-border bg-card py-12">
        <div className="container mx-auto px-4">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-3xl font-bold text-foreground md:text-4xl" style={{ fontFamily: "Impact, sans-serif" }}>
              Now showing
            </h2>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="gap-2 bg-transparent">
                  {selectedCity}
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem onClick={() => setSelectedCity("Seattle")}>Seattle</DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectedCity("San Jose")}>San Jose</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="relative">
            <div className="flex flex-col gap-6 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-border">
              {sampleMovies.map((movie) => (
                <div key={movie.id} className="w-full">
                  <div className="group overflow-hidden rounded-lg bg-card shadow-lg border border-border transition-transform hover:scale-[1.02]">
                    <div className="p-4">
                      <h3
                        className="mb-2 text-lg font-semibold text-foreground line-clamp-2"
                        style={{ fontFamily: "Impact, sans-serif" }}
                      >
                        {movie.title}
                      </h3>
                      <p className="mb-1 text-sm text-muted-foreground">{movie.runtime}</p>
                      <p className="mb-2 text-sm font-medium text-primary">{movie.rating}</p>
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <MapPin className="h-3 w-3" />
                        <span className="line-clamp-1">{movie.theater.split(",")[0]}</span>
                      </div>
                      <p className="mt-2 text-sm font-medium text-foreground">{movie.showtimes[0]}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Hero Section */}
      <section className="border-b border-border bg-muted/30">
        <div className="container mx-auto px-4 py-12 md:py-16">
          <div className="mx-auto max-w-2xl text-center">
            <h2
              className="mb-3 text-3xl font-bold tracking-tight text-foreground md:text-4xl text-balance"
              style={{ fontFamily: "Impact, sans-serif" }}
            >
              Discover Movies in Your Area
            </h2>
            <p className="mb-6 text-base text-muted-foreground md:text-lg text-pretty">
              Enter your zip code to find the latest films showing near you
            </p>

            {/* Search Form */}
            <form onSubmit={handleSearch} className="mx-auto max-w-md">
              <div className="flex gap-2">
                <div className="relative flex-1">
                  <MapPin className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Enter US zip code (e.g., 90210)"
                    value={zipCode}
                    onChange={(e) => setZipCode(e.target.value)}
                    className="pl-10 h-11 bg-background text-foreground"
                    maxLength={5}
                  />
                </div>
                <Button type="submit" size="lg" className="h-11 px-6">
                  <Search className="mr-2 h-4 w-4" />
                  Search
                </Button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* Results Section */}
      {movies.length > 0 && (
        <section className="py-12 md:py-16">
          <div className="container mx-auto px-4">
            <div className="mb-8 flex items-center justify-between">
              <div>
                <h3
                  className="text-2xl font-bold text-foreground md:text-3xl"
                  style={{ fontFamily: "Impact, sans-serif" }}
                >
                  Now Showing in {searchedZip}
                </h3>
                <p className="mt-2 text-muted-foreground">{movies.length} movies found in your area</p>
              </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {movies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Empty State */}
      {movies.length === 0 && searchedZip === "" && (
        <section className="py-16 md:py-24">
          <div className="container mx-auto px-4 text-center">
            <div className="mx-auto max-w-md">
              <div className="mb-6 inline-flex h-20 w-20 items-center justify-center rounded-full bg-secondary">
                <Search className="h-10 w-10 text-primary" />
              </div>
              <h3 className="mb-3 text-xl font-semibold text-foreground" style={{ fontFamily: "Impact, sans-serif" }}>
                Start Your Search
              </h3>
              <p className="text-muted-foreground">
                Enter your zip code above to discover movies playing in theaters near you
              </p>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}
