import { ref } from "vue";
import { defineStore } from "pinia";
import { UserDetails } from "../types";
import axios from "axios";

export const useUserStore = defineStore("user", () => {
  const user = ref<UserDetails>();

  const getUser = async () => {
    try {
      const response = await axios.get<UserDetails | {
        signup: "osu" | "twitch"
      }>("/user/me");

      if ("signup" in response.data) {
        return response.data.signup;
      }

      user.value = response.data;
    } catch {

    }
  }

  const logoutUser = async () => {
    try {
      await axios.get("/user/logout");
      user.value = undefined;
    } finally {
      user.value = undefined;
    }
  }

  const deleteUser = async () => {
    try {
      await axios.delete("/user/me");
      user.value = undefined;
    } finally {
      user.value = undefined;
    }
  }

  return {
    user,
    getUser,
    logoutUser,
    deleteUser
  }
})
