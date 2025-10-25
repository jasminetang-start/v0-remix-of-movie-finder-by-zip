"use client"
import Image from "next/image"
import { useState } from "react"
import { MapPin, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
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
    city: "Vancouver BC",
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
    city: "Vancouver BC",
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
    city: "Vancouver BC",
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
    city: "Vancouver BC",
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
    city: "Seattle",
  },
]

export default function MovieResearchPage() {
  const [selectedCity, setSelectedCity] = useState("Seattle")

  const filteredMovies = sampleMovies.filter((movie) => movie.city === selectedCity)

  const trackCardClick = async (movieTitle: string) => {
    try {
      const scriptUrl = process.env.NEXT_PUBLIC_GOOGLE_SCRIPT_URL

      if (!scriptUrl) {
        console.warn("[v0] Google Script URL not configured")
        return
      }

      const params = new URLSearchParams({
        element_name: movieTitle,
        element_type: "movie_card",
        page_url: window.location.href,
        user_agent: navigator.userAgent,
        referrer: document.referrer || "direct",
      })

      await fetch(`${scriptUrl}?${params.toString()}`, {
        method: "POST",
        mode: "no-cors",
      })
    } catch (error) {
      console.error("[v0] Failed to track card click:", error)
    }
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
                <DropdownMenuItem onClick={() => setSelectedCity("Vancouver BC")}>Vancouver BC</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          {filteredMovies.length > 0 ? (
            <div className="relative">
              <div className="flex flex-col gap-6 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-border">
                {filteredMovies.map((movie) => (
                  <div key={movie.id} className="w-full">
                    <div
                      className="group overflow-hidden rounded-lg bg-card shadow-lg border border-border transition-transform hover:scale-[1.02] cursor-pointer"
                      onClick={() => trackCardClick(movie.title)}
                    >
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
          ) : (
            <div className="py-12 text-center">
              <p className="text-lg text-muted-foreground">Check back soon for showtimes in {selectedCity}!</p>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}
