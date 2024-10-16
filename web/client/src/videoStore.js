import { defineStore } from 'pinia';

export const useVideoStore = defineStore('video', {
  state: () => ({
    videoBlob: null,
  }),
});