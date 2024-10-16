<script setup>
import { ref, watch, onMounted, onUnmounted } from "vue";

const camera = ref(null);
// const picture = ref(null);
const mediaRecorder = ref(null);
const recordedChunks = ref([]);
const isRecording = ref(false);

const getVideo = () => {
    navigator.mediaDevices
        .getUserMedia({ video: true })
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

// const takeSnapshot = () => {
//     const width = 500;
//     const height = 500;
//
//     var video = camera.value;
//
//     picture.value.width = width;
//     picture.value.height = height;
//
//     var ctx = picture.value.getContext("2d");
//     // ctx.translate(width, 0); // Move the context to the right
//     // ctx.scale(-1, 1); // Flip the context horizontally
//     ctx.drawImage(video, 0, 0, width, height);
// };

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
  const videoFile = new File([blob], "recorded_video.webm", { type: "video/webm" });
  emit("videoRecorded", videoFile)
}

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
  <p>TEST TEXT TEST TEXT</p>
    <div class="camera">
        <div class="camera__wrapper">
            <video ref="camera" class="flipped"></video>
        </div>

      <button @click="isRecording ? stopRecording() : startRecording()">
            {{ isRecording ? "Stop Recording" : "Start Recording" }}
      </button>
      <button @click="saveRecording" :disabled="isRecording">Save Recording</button>

<!--        <button @click="takeSnapshot">SNAP!</button>-->
    </div>

<!--    <div class="result">-->
<!--        <canvas ref="picture"></canvas>-->
<!--    </div>-->
</template>

<style lang="scss" scoped>
.camera {
    background-color: rgba(0, 255, 255, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;

    &__wrapper {
        width: 60%;
        overflow: hidden;

        video {
            width: 100%;
            height: auto;
        }
    }
}

.flipped {
    transform: scaleX(-1);
}

//.result {
//    margin-top: 2rem;
//}
</style>
