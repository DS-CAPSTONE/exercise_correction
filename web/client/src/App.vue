<script setup>
</script>

<template>
    <div class="site-container">
        <!-- Navbar -->
        <nav>
            <RouterLink :to="{ name: 'Home' }" class="nav__header">
                DS_CAPSTONE EXCERCISE CORRECTION
            </RouterLink>
        </nav>

        <!-- Main Content -->
        <main>
            <!-- Page View -->
            <RouterView />
        </main>

        <!-- Footer -->
<!--        <footer>-->
<!--            <a-->
<!--                href="https://twitter.com/ngohquocbao1010"-->
<!--                target="_blank"-->
<!--                class="twitter"-->
<!--            >-->
<!--                @NgoQuocBao-->
<!--            </a>-->

<!--            <a-->
<!--                href="https://github.com/NgoQuocBao1010/Exercise-Correction"-->
<!--                target="_blank"-->
<!--                class="github"-->
<!--            >-->
<!--                <i class="fa-brands fa-github"></i>-->
<!--            </a>-->
<!--        </footer>-->
    </div>
</template>

<style lang="scss">
body {
    .site-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    nav {
        margin: 3rem 0;
        text-align: center;

        .nav__header {
            font-size: 2rem;
            font-family: var(--font-family);
            font-weight: 700;
            //text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--primary-color);

              background-image: linear-gradient(
                to right,
                #8958BAFF,
                #8958ba 50%,
                #9E6DD3FF 50%
              );
              background-size: 200% 100%;
              background-position: -100%;
              display: inline-block;
              padding: 5px 0;
              position: relative;
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
              transition: all 0.3s ease-in-out;

            &:before {
              content: '';
              background: #8958BAFF;
              display: block;
              position: absolute;
              bottom: -3px;
              left: 0;
              width: 0;
              height: 3px;
              transition: all 0.3s ease-in-out;
            }

            &:hover {
             background-position: 0;
            }

            &:hover::before {
              width:100%;
            }
        }
    }

    main {
        margin-inline: auto;
        width: 90vw;
    }

    footer {
        margin-top: auto;
        margin-inline: auto;
        width: 90vw;
        border-top: 1px solid var(--primary-color);
        padding: 0.3rem 0;
        text-align: center;

        a {
            font-family: var(--font-family);
            color: var(--primary-color);
        }

        .twitter {
            font-weight: 700;
        }

        .github {
            font-size: 1.2rem;
            margin-left: 1rem;
        }
    }
}
</style>
