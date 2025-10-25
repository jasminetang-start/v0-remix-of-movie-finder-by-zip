"use client"

import { Clock, Star, MapPin } from "lucide-react"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface Movie {
  id: number
  title: string
  genre: string
  rating: string
  runtime: string
  theater: string
  showtimes: string[]
  image: string
}

interface MovieCardProps {
  movie: Movie
}

export function MovieCard({ movie }: MovieCardProps) {
  const trackCardClick = async () => {
    try {
      const scriptUrl = process.env.NEXT_PUBLIC_GOOGLE_SCRIPT_URL

      if (!scriptUrl) {
        console.warn("[v0] Google Script URL not configured")
        return
      }

      const params = new URLSearchParams({
        element_name: movie.title,
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
    <Card
      className="group overflow-hidden transition-all hover:shadow-lg hover:shadow-primary/10 cursor-pointer"
      onClick={trackCardClick}
    >
      <CardContent className="p-4">
        <div className="mb-3 flex items-start justify-between gap-2">
          <h3 className="text-xl font-bold text-foreground line-clamp-2" style={{ fontFamily: "Impact, sans-serif" }}>
            {movie.title}
          </h3>
          <Badge className="bg-secondary text-foreground flex-shrink-0">
            <Star className="mr-1 h-3 w-3 fill-primary text-primary" />
            {movie.rating}
          </Badge>
        </div>

        <div className="mb-3 flex items-center gap-3 text-sm text-muted-foreground">
          <Badge variant="outline" className="border-primary/30 text-primary">
            {movie.genre}
          </Badge>
          <div className="flex items-center gap-1">
            <Clock className="h-3.5 w-3.5" />
            {movie.runtime}
          </div>
        </div>

        <div className="mb-3 flex items-start gap-2 text-sm">
          <MapPin className="mt-0.5 h-4 w-4 flex-shrink-0 text-muted-foreground" />
          <span className="text-muted-foreground line-clamp-2">{movie.theater}</span>
        </div>

        <div>
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Showtimes</p>
          <div className="flex flex-wrap gap-2">
            {movie.showtimes.map((time, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                className="h-8 text-xs hover:bg-primary hover:text-primary-foreground bg-transparent"
              >
                {time}
              </Button>
            ))}
          </div>
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0">
        <Button className="w-full" size="lg">
          Get Tickets
        </Button>
      </CardFooter>
    </Card>
  )
}
