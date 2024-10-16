<script setup>
import { ref, watch, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useVideoStore} from "@/videoStore";

const router = useRouter();
const videoStore = useVideoStore()
const camera = ref(null);
const mediaRecorder = ref(null);
const recordedChunks = ref([]);
const isRecording = ref(false);

const getVideo = () => {
    navigator.mediaDevices
        .getUserMedia({
          video: {
            width: { ideal: 1280 },
            height: { ideal: 832 },
            // frameRate: { ideal: 30 },
            facingMode: "user",
          },
        })
        .then((stream) => {
            let video = camera.value;
            video.srcObject = stream;
            video.play();
            mediaRecorder.value = new MediaRecorder(stream);
            mediaRecorder.value.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.value.push(event.data);
                }
            };
        })
        .catch((err) => console.log(err));
};

const startRecording = () => {
    recordedChunks.value = [];
    mediaRecorder.value.start();
    isRecording.value = true;
};

const stopRecording = () => {
    mediaRecorder.value.stop();
    isRecording.value = false;
};

const saveRecording = () => {
  const blob = new Blob(recordedChunks.value, { type: "video/webm" });
  console.log('Blob:', blob); // Should show type "video/webm"

  // No need to create a File object here unless necessary
  videoStore.videoBlob = blob;
  router.push("/video");
};

watch(camera, () => {
    getVideo();
});

onMounted(() => {
    getVideo();
});

onUnmounted(() => {
    if (mediaRecorder.value && mediaRecorder.value.state !== "inactive") {
        mediaRecorder.value.stop();
    }
});
</script>

<template>
    <div class="camera">
        <div class="camera__wrapper">
            <video ref="camera" class="flipped"></video>
        </div>

        <button @click="isRecording ? stopRecording() : startRecording()">
            {{ isRecording ? "Stop Recording" : "Start Recording" }}
        </button>
        <button @click="saveRecording" :disabled="isRecording">Save Recording</button>
    </div>
</template>

<style lang="scss" scoped>
.camera {
    //background-color: rgba(0, 255, 255, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;

    &__wrapper {
        width: 100%;
        overflow: hidden;

        video {
            width: 100%;
            height: auto;
        }
    }
}

.flipped {
    transform: scaleX(-1); /* Flip the video horizontally */
}
</style>