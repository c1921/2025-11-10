export interface GameTime {
  day: number
  hour: number
  time_string: string
  running: boolean
  speed: number
}

export interface Item {
  item_id: string
  name: string
  description: string
  category: string
  rarity: string
  stackable: boolean
  max_stack: number
  weight: number
  value: number
  effects: Record<string, number>
}

export interface ItemStack {
  item: Item
  quantity: number
}

export interface Inventory {
  max_slots: number
  used_slots: number
  items: ItemStack[]
}

export interface Character {
  id: string
  name: string
  gender: string
  age_years: number
  age_days: number
  age_string: string
  fatigue: number
  hunger: number
  mood: number
  current_action: string
  action_duration: number
  status_text: string
  inventory: Inventory
}

export interface GameUpdate {
  time: GameTime
  characters: Character[]
  public_storage: Inventory
}

export interface WebSocketMessage {
  type: 'game_update' | 'speed_update' | 'status_update'
  data: GameUpdate | GameTime
}
