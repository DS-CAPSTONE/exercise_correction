<script setup>
import { ref, watch } from "vue";

const camera = ref(null);
const picture = ref(null);

const getVideo = () => {
    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
            let video = camera.value;
            video.srcObject = stream;
            video.play();
            video.onloadedmetadata = () => {
                console.log(`Video Width: ${video.videoWidth}, Video Height: ${video.videoHeight}`);
            };
        })
        .catch((err) => console.log(err));
};

const takeSnapshot = () => {
    const width = 100;
    const height = width * (camera.value.videoHeight / camera.value.videoWidth);

    let video = camera.value;

    picture.value.width = width;
    picture.value.height = height;

    let ctx = picture.value.getContext("2d");
    ctx.drawImage(video, 0, 0, width, height);
};

watch(camera, () => {
    getVideo();
});
</script>

<template>
    <div class="camera">
        <div class="camera__wrapper">
            <video ref="camera"></video>
        </div>
<!--        <div class="snapButtonContainer">-->
<!--            <button @click="takeSnapshot" class="snapButton">SNAP!</button>-->
<!--        </div>-->
    </div>
<!--    <div class="result">-->
<!--        <canvas ref="picture"></canvas>-->
<!--    </div>-->
</template>

<style lang="scss" scoped>
.camera {
    background-color: rgba(0, 255, 255, 0.5);
    //display: flex;
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

.snapButtonContainer {
    height: 30px;
    display: flex;
    justify-content: center;
}

.snapButton {
  width: 60px;
  height: 20px;
}

.result {
    //margin-top: 2rem;
}
</style>
