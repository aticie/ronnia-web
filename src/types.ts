export interface Setting {
  name: string,
  type: "toggle" | "value" | "range",
  description: string
}

export interface SettingValue extends Setting {
  value: number,
  type: "value"
}

export interface SettingRange extends Setting {
  value: [number, number],
  type: "range"
}

export interface SettingToggle extends Setting {
  value: 1 | 0,
  type: "toggle"
}

export type Settings = (SettingValue | SettingRange | SettingToggle)[];

export interface UserDetails {
  osuId: number,
  osuUsername: string,
  osuAvatarUrl: string,
  twitchId: number,
  twitchUsername: string,
  twitchAvatarUrl: string,
  isLive: boolean
}
