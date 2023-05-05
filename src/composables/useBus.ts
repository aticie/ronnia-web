import { useEventBus } from "@vueuse/core";

export interface Notification {
  id?: number,
  title: string,
  description?: string
}

export const useBus = () => {
  const bus = useEventBus<Notification>("notification");
  return bus;
}
