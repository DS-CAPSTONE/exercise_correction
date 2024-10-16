<script setup>

import { ref } from "vue";
import axios from "axios";

import LiveStreamingZone from "../components/LiveStreamingZone.vue";
import LiveStreamingLoading from "../components/LiveStreamingLoading.vue";
import Result from "@/components/Result.vue";

const apiUrl = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:8000";

const EXERCISES = ["squat", "plank", "bicep_curl", "lunge"];

const submitData = ref({
    videoFile: null, // LiveStreaming 에서는 녹화 영상 저장용으로 사용?
    exerciseType: null,
});

const processedData = ref(null);
const isProcessing = ref(false);

const videoIsNotReady = ref(null);

// 영상 보내주는 용도의 함수인데 라이브 스트리밍에서는 필요 없음.
// const uploadToServer = async () => {};

</script>

<template>
    <div id="LiveStreamingTitle">
<!--        <h1>Live Streaming Page</h1>-->
        <!-- Add your live streaming content here -->
    </div>
    <section class="LiveCameraSection">
      <LiveStreamingZone
        v-show="!videoIsNotReady"
      />
      <LiveStreamingLoading v-show="videoIsNotReady"/>

<!--      <div class="right-container">-->
<!--          &lt;!&ndash; exercises selection &ndash;&gt;-->
<!--          <div class="exercises-container">-->
<!--              <p-->
<!--                  class="exercise"-->
<!--                  v-for="exercise in EXERCISES"-->
<!--                  :class="{ active: submitData.exerciseType == exercise }"-->
<!--                  @click="submitData.exerciseType = exercise"-->
<!--              >-->
<!--                  {{ exercise }}-->
<!--              </p>-->
<!--          </div>-->

<!--&lt;!&ndash;          <button class="process-btn" @click="uploadToServer">&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;                <span>Process!</span>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;                  <i class="fa-solid fa-play"></i>&ndash;&gt;-->
<!--&lt;!&ndash;          </button>&ndash;&gt;-->
<!--      </div>-->
    </section>

<!--        &lt;!&ndash; Results section &ndash;&gt;-->
<!--    <Result v-if="processedData" :data="processedData" />-->

    <p class="video-size-warning">The size of recorded video must be over the size 2.5MB!</p>
</template>

<style lang="scss" scoped>
.LiveCameraSection {
    display: flex;
    justify-content: center; /* Center the camera section horizontally */
    align-items: center; /* Center the camera section vertically */
    //gap: 1rem;

    * {
        //flex: 1;
    }

    LiveStreamingZone {
        flex-basis: 90%;
        //flex-grow: 8;
    }

    //.right-container {
    //    display: flex;
    //    flex-direction: column;
    //    //width: 100%;
    //    flex-basis: 20%;
    //    //flex-grow: 2;
    //
    //    .exercises-container {
    //        display: flex;
    //        flex-wrap: wrap;
    //        gap: 1rem;
    //        margin-bottom: 1rem;
    //
    //        .exercise {
    //            display: flex;
    //            justify-content: center;
    //            align-items: center;
    //            padding: 1rem 0;
    //            flex: 45%;
    //            color: var(--secondary-color);
    //            text-transform: uppercase;
    //            border: 3px solid var(--primary-color);
    //            border-radius: 0.3rem;
    //            cursor: pointer;
    //            transition: all 0.25s ease;
    //
    //            &:hover {
    //                box-shadow: 0 6px 18px 0 rgba(#000, 0.1);
    //                transform: translateY(-6px);
    //            }
    //
    //            &.active {
    //                background-color: var(--primary-color);
    //                color: whitesmoke;
    //                font-weight: 700;
    //            }
    //        }
    //    }
    //
    //    //.process-btn {
    //    //    border: none;
    //    //    background-color: var(--primary-color);
    //    //    padding: 1.25rem 0;
    //    //
    //    //    color: whitesmoke;
    //    //    font-size: 2rem;
    //    //    font-weight: 700;
    //    //    cursor: pointer;
    //    //    border-radius: 8px;
    //    //    transition: all 0.25s ease;
    //    //
    //    //    &:hover {
    //    //        box-shadow: 0 6px 18px 0 rgba(#000, 0.1);
    //    //        color: var(--primary-color);
    //    //        border-color: transparent;
    //    //        background-color: transparent;
    //    //    }
    //    //}
    //}
}

.video-size-warning {
    text-align: center;
    margin-top: 1rem;
    font-size: 1rem;
    //color: red;
}
</style>