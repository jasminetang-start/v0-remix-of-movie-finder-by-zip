"use client"
import Image from "next/image"
import { useState } from "react"
import { MapPin, ChevronDown, Star, Clock, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import moviesData from "@/data/movies.json"

interface MovieShowtime {
  show_date: string
  show_time: string
}

interface MovieRatings {
  imdb?: string
  rotten_tomatoes?: string
  metacritic?: string
  imdb_rating?: string
  imdb_votes?: string
}

interface MovieInfo {
  title: string
  url: string
  image_url: string
  country: string | null
  year: number | null
  duration: number | null
  director: string | null
  imdb_id?: string
  plot?: string
  genre?: string
  rated?: string
  actors?: string
  writer?: string
  language?: string
  awards?: string
  poster_omdb?: string
  ratings?: MovieRatings
  box_office?: string
}

interface MovieData {
  movie: MovieInfo
  cinema_id: string
  showtimes: MovieShowtime[]
  scraped_at: string
}

interface CinemaShowtimes {
  cinema_id: string
  showtimes: MovieShowtime[]
}

interface ConsolidatedMovie {
  movie: MovieInfo
  cinemas: CinemaShowtimes[]
}

const cinemaToCity: Record<string, string> = {
  SIFF_DOWNTOWN: "Seattle",
  SIFF_UPTOWN: "Seattle",
  SIFF_FILM_CENTER: "Seattle",
}

const getCinemaName = (cinemaId: string): string => {
  const cinemaNames: Record<string, string> = {
    SIFF_DOWNTOWN: "SIFF Cinema Downtown",
    SIFF_UPTOWN: "SIFF Cinema Uptown",
    SIFF_FILM_CENTER: "SIFF Film Center",
  }
  return cinemaNames[cinemaId] || cinemaId
}

const formatShowtimes = (showtimes: MovieShowtime[]): string => {
  if (showtimes.length === 0) return "No showtimes available"

  // Group showtimes by date
  const groupedByDate: Record<string, string[]> = {}
  showtimes.forEach((showtime) => {
    if (!groupedByDate[showtime.show_date]) {
      groupedByDate[showtime.show_date] = []
    }
    groupedByDate[showtime.show_date].push(showtime.show_time)
  })

  // Format the first date's showtimes
  const firstDate = Object.keys(groupedByDate)[0]
  const times = groupedByDate[firstDate].slice(0, 3).join(", ")
  const moreCount = showtimes.length - 3

  return moreCount > 0 ? `${times} +${moreCount} more` : times
}

export default function MovieResearchPage() {
  const [selectedCity, setSelectedCity] = useState("Seattle")

  const consolidateMovies = (movies: MovieData[]): ConsolidatedMovie[] => {
    const movieMap = new Map<string, ConsolidatedMovie>()

    movies.forEach((movieData) => {
      const { movie, cinema_id, showtimes } = movieData
      const movieUrl = movie.url

      if (movieMap.has(movieUrl)) {
        // Add cinema showtimes to existing movie
        const existing = movieMap.get(movieUrl)!
        existing.cinemas.push({ cinema_id, showtimes })
      } else {
        // Create new consolidated movie entry
        movieMap.set(movieUrl, {
          movie,
          cinemas: [{ cinema_id, showtimes }],
        })
      }
    })

    return Array.from(movieMap.values())
  }

  const filteredMovies = (moviesData as MovieData[]).filter(
    (movieData) => cinemaToCity[movieData.cinema_id] === selectedCity,
  )

  const consolidatedMovies = consolidateMovies(filteredMovies)

  const handleCardClick = async (movieTitle: string, movieUrl: string) => {
    try {
      const scriptUrl = process.env.NEXT_PUBLIC_GOOGLE_SCRIPT_URL

      if (scriptUrl) {
        const params = new URLSearchParams({
          element_name: movieTitle,
          element_type: "movie_card",
          page_url: window.location.href,
          user_agent: navigator.userAgent,
          referrer: document.referrer || "direct",
        })

        // Fire and forget tracking
        fetch(`${scriptUrl}?${params.toString()}`, {
          method: "POST",
          mode: "no-cors",
        }).catch((error) => console.error("[v0] Failed to track card click:", error))
      }
    } catch (error) {
      console.error("[v0] Failed to track card click:", error)
    }

    // Redirect to movie URL
    window.open(movieUrl, "_blank", "noopener,noreferrer")
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

      {/* Now showing section */}
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
          {consolidatedMovies.length > 0 ? (
            <div className="relative">
              <div className="flex flex-col gap-6 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-border">
                {consolidatedMovies.map((consolidatedMovie, index) => {
                  const { movie, cinemas } = consolidatedMovie
                  return (
                    <div key={`${movie.url}-${index}`} className="w-full">
                      <div
                        className="group overflow-hidden rounded-lg bg-card shadow-lg border border-border transition-transform hover:scale-[1.02] cursor-pointer"
                        onClick={() => handleCardClick(movie.title, movie.url)}
                      >
                        <div className="flex flex-col md:flex-row gap-4 p-4">
                          {movie.image_url && (
                            <div className="relative w-full md:w-48 h-64 md:h-auto flex-shrink-0">
                              <Image
                                src={movie.image_url || "/placeholder.svg"}
                                alt={movie.title}
                                fill
                                className="object-cover rounded-md"
                              />
                            </div>
                          )}

                          <div className="flex-1 space-y-3">
                            <div>
                              <div className="flex items-start justify-between gap-2">
                                <h3
                                  className="text-xl font-bold text-foreground mb-2"
                                  style={{ fontFamily: "Impact, sans-serif" }}
                                >
                                  {movie.title}
                                </h3>
                                <ExternalLink className="h-5 w-5 text-muted-foreground flex-shrink-0 mt-1" />
                              </div>

                              <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground mb-2">
                                {movie.year && <span>{movie.year}</span>}
                                {movie.duration && (
                                  <>
                                    <span>•</span>
                                    <div className="flex items-center gap-1">
                                      <Clock className="h-3 w-3" />
                                      <span>{movie.duration} min</span>
                                    </div>
                                  </>
                                )}
                                {movie.rated && (
                                  <>
                                    <span>•</span>
                                    <Badge variant="outline">{movie.rated}</Badge>
                                  </>
                                )}
                              </div>

                              {movie.genre && <p className="text-sm text-muted-foreground mb-2">{movie.genre}</p>}

                              {movie.director && (
                                <p className="text-sm text-foreground mb-2">
                                  <span className="font-medium">Director:</span> {movie.director}
                                </p>
                              )}

                              {movie.actors && (
                                <p className="text-sm text-foreground mb-2">
                                  <span className="font-medium">Cast:</span> {movie.actors}
                                </p>
                              )}

                              {movie.plot && (
                                <p className="text-sm text-muted-foreground line-clamp-2 mb-2">{movie.plot}</p>
                              )}

                              {movie.ratings && (
                                <div className="flex flex-wrap items-center gap-3 mb-2">
                                  {movie.ratings.imdb && (
                                    <div className="flex items-center gap-1 text-sm">
                                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                                      <span className="font-medium">IMDb:</span>
                                      <span>{movie.ratings.imdb}</span>
                                    </div>
                                  )}
                                  {movie.ratings.rotten_tomatoes && (
                                    <div className="flex items-center gap-1 text-sm">
                                      <span className="font-medium">RT:</span>
                                      <span>{movie.ratings.rotten_tomatoes}</span>
                                    </div>
                                  )}
                                  {movie.ratings.metacritic && (
                                    <div className="flex items-center gap-1 text-sm">
                                      <span className="font-medium">Metacritic:</span>
                                      <span>{movie.ratings.metacritic}</span>
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>

                            <div className="pt-2 border-t border-border space-y-3">
                              {cinemas.map((cinema, cinemaIndex) => (
                                <div key={`${cinema.cinema_id}-${cinemaIndex}`}>
                                  <div className="flex items-center gap-1 text-sm text-muted-foreground mb-1">
                                    <MapPin className="h-4 w-4" />
                                    <span className="font-medium">{getCinemaName(cinema.cinema_id)}</span>
                                  </div>
                                  <p className="text-sm font-medium text-foreground ml-5">
                                    {formatShowtimes(cinema.showtimes)}
                                  </p>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )
                })}
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
