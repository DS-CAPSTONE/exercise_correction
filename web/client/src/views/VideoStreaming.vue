<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useVideoStore } from "@/videoStore";

import Dropzone from "../components/Dropzone.vue";
import DropzoneLoading from "../components/DropzoneLoading.vue";
import Result from "../components/Result.vue";

const apiUrl = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:8000";

const EXERCISES = ["squat", "plank", "bicep_curl", "lunge"];

const submitData = ref({
    videoFile: null,
    exerciseType: null,
});
const processedData = ref(null);
const isProcessing = ref(false);

const videoStore = useVideoStore();
const videoBlob = videoStore.videoBlob;

let videoURLRef = ref(null);

// const uploadToServer = async () => {
//   if (!submitData.value.videoFile) {
//     alert("No video selected");
//     return;
//   }
//
//   if (!submitData.value.exerciseType) {
//     alert("No exercise type selected");
//     return;
//   }
//
//   processedData.value = null;
//   try {
//     isProcessing.value = true;
//     const {data} = await axios.post(
//         `${apiUrl}/api/video/upload?type=${submitData.value.exerciseType}`,
//         {file: submitData.value.videoFile},
//         {
//           headers: {
//             "Content-Type": "multipart/form-data",
//           },
//         }
//     );
//     processedData.value = data;
//   } catch (e) {
//     console.error("Error: ", e);
//   } finally {
//     isProcessing.value = false;
//   }
// };

const uploadToServer = async () => {
  if (!submitData.value.videoFile) {
    alert("No video selected");
    return;
  }

  if (!submitData.value.exerciseType) {
    alert("No exercise type selected");
    return;
  }

  processedData.value = null;
  try {
    isProcessing.value = true;

    const formData = new FormData();
    formData.append('file', submitData.value.videoFile);

    // Log FormData entries
    for (let [key, value] of formData.entries()) {
        console.log(`${key}:`, value);
    }

    const { data } = await axios.post(
      `${apiUrl}/api/video/upload?type=${submitData.value.exerciseType}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    processedData.value = data;
  } catch (e) {
    console.error("Error: ", e);
    if (e.response && e.response.data) {
      console.error("Server response:", e.response.data);
    }
  } finally {
    isProcessing.value = false;
  }
};


onMounted(() => {
  if (!submitData.value.videoFile && videoBlob) {
    const videoFile = new File([videoBlob], "recorded_video.webm", { type: "video/webm" });
    console.log('Retrieved Video File: ', videoFile);

    submitData.value.videoFile = videoFile;
    console.log('submitData.value.videoFile: ', videoFile);

    const videoURL = URL.createObjectURL(videoFile);
    videoURLRef.value = videoURL;
    console.log('Video URL:', videoURL);

    // Optionally, clear the videoBlob from the store to free up memory
    // videoStore.videoBlob = null;
  } else {
    console.error('No video data available.');
  }
});

</script>

<template>
  <!-- Input section -->
  <section class="input-section">
    <Dropzone
        v-show="!isProcessing"
        @file-uploaded="(file) => (submitData.videoFile = file)"
        :external-file="submitData.videoFile"
    />
    <DropzoneLoading v-show="isProcessing"/>

    <div class="right-container">
      <!-- exercises selection -->
      <div class="exercises-container">
        <p
            class="exercise"
            v-for="exercise in EXERCISES"
            :class="{ active: submitData.exerciseType == exercise }"
            @click="submitData.exerciseType = exercise"
        >
          {{ exercise }}
        </p>
      </div>

      <button class="process-btn" @click="uploadToServer">
        <i class="fa-solid fa-play"></i>
      </button>
    </div>
  </section>

  <!-- Results section -->
  <Result v-if="processedData" :data="processedData"/>

  <!-- Video preview -->
<!--  <video v-if="videoURLRef" controls :src="videoURLRef" width="640" height="480"></video>-->
</template>



<style lang="scss" scoped>
.input-section {
  display: flex;
  gap: 1rem;

  * {
    flex: 1;
  }

  .right-container {
    display: flex;
    flex-direction: column;
    width: 100%;

    .exercises-container {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1rem;

      .exercise {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem 0;
        flex: 45%;
        color: var(--secondary-color);
        text-transform: uppercase;
        border: 3px solid var(--primary-color);
        border-radius: 0.3rem;
        cursor: pointer;
        transition: all 0.25s ease;

        &:hover {
          box-shadow: 0 6px 18px 0 rgba(#000, 0.1);
          transform: translateY(-6px);
        }

        &.active {
          background-color: var(--primary-color);
          color: whitesmoke;
          font-weight: 700;
        }
      }
    }

    .process-btn {
      border: none;
      background-color: var(--primary-color);
      padding: 1.25rem 0;

      color: whitesmoke;
      font-size: 2rem;
      font-weight: 700;
      cursor: pointer;
      border-radius: 8px;
      transition: all 0.25s ease;

      &:hover {
        box-shadow: 0 6px 18px 0 rgba(#000, 0.1);
        color: var(--primary-color);
        border-color: transparent;
        background-color: transparent;
      }
    }
  }
}
</style>