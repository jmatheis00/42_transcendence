<script setup>
import { useI18n } from 'vue-i18n'

const profileLinks = [
	{ link: 'https://github.com/Anoukmch', name: 'amechain' },
	{ link: 'https://github.com/jharrach', name: 'jharrach' },
	{ link: 'https://github.com/jmatheis00', name: 'jmatheis' },
	{ link: 'https://github.com/nuno101', name: 'nlouro' },
	{ link: 'https://github.com/PythonGermany', name: 'rburgsta' }
]
</script>

<template>
    <footer class="container-fluid p-3 text-center text-white">
		<h6 class="text-uppercase fw-bold pb-1">{{useI18n().t('home.connectOnGithub')}}</h6>
		<div class="d-flex flex-wrap justify-content-center">
			<p class="mx-md-4 mx-2" v-for="(link, index) in profileLinks" :key="index">
				<i class="bi bi-github"></i> <a class="link-opacity-50-hover text-white" :href="link.link">{{ link.name }}</a>
			</p>
		</div>
		<div>
			<i class="bi bi-github"></i> <a class="link-opacity-50-hover text-white" href="https://github.com/nuno101/transcendence">{{useI18n().t('home.ourTranscendenceProject')}}</a>
		</div>
	</footer>
</template>

<style scoped>
footer {
    background-color: rgba(0, 0, 0, 0.5);
    bottom: 0;
    left: 0;
    position: absolute;
    width: 100%;
}
</style>