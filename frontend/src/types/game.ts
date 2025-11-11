export interface GameTime {
  day: number
  hour: number
  time_string: string
  running: boolean
  speed: number
}

export interface Character {
  name: string
  gender: string
  fatigue: number
  hunger: number
  mood: number
  status_text: string
}

export interface GameUpdate {
  time: GameTime
  characters: Character[]
}

export interface WebSocketMessage {
  type: 'game_update' | 'speed_update' | 'status_update'
  data: GameUpdate | GameTime
}
