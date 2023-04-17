interface Setting {
  id: number,
  key: string,
  description: string
}

export interface SettingToggle extends Setting {
  default_value: number,
  value: number,
  type: "toggle" | "value",
}

export interface SettingRange extends Setting {
  default_low: number,
  default_high: number,
  range_start: number,
  range_end: number
  type: "range" 
}

export type SettingType = SettingRange | SettingToggle;

export interface UserDetails {
  command: string,
  osu_username: string,
  osu_id: number,
  twitch_username: string,
  twitch_id: string,
  avatar_url: string,
  user_id: number,
  username: string,
  exp: number,
  excluded_users: string[],
  settings: SettingType[]
}
