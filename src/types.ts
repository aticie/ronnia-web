type SettingTypes = "toggle" | "range" | "value";

interface Setting {
  id: number,
  key: string,
  default_value: number,
  description: string,
  type: SettingTypes,
  value: number
}

interface SettingRange extends Omit<Omit<Setting, 'default_value'>, 'value'> {
  default_low: number,
  default_high: number,
  range_start: number,
  range_end: number
}

interface UserDetails {
  command: string,
  osu_username: string,
  osu_id: number,
  twitch_username: string,
  twitch_id: string,
  avatar_url: string,
  user_id: string,
  username: string,
  exp: number,
  excluded_users: string[],
  settings: Setting | SettingRange[]
}
