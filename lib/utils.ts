import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}


export function getAssetPath(path: string) {
  const basePath = '/movie-finder-by-city'
  return `${basePath}${path}`
}