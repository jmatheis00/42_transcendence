<template>
	<div class="dropdown">
		<button type="button" 
			class="btn btn-outline-light px-2"
			data-bs-toggle="dropdown"
			aria-expanded="false"
			@click="toggleDropdown"
		>
			<i class="bi bi-bell-fill"></i>
			<span v-if="Notifications.messages.value.length > 0 && dropdownShown > 0"
				class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger text-light">
				{{dropdownShown}}
			</span>
		</button>
		<ul class="p-0 dropdown-menu" @click="toggleDropdown">
			<li v-if="storedNotifications.length <= 0 && Notifications.messages.value.length <= 0">{{ useI18n().t(`notif.noNotifications`) }}</li>
			<li v-for="(item, index) in Notifications.messages.value.slice().reverse()" :key="index">
			<div class="dropdown-item d-flex align-items-center me-2">
				{{ useI18n().t(`notif.${item.content}`) }}
				<button type="button" class="btn btn-sm btn-outline-dark ms-auto" aria-label="Close" @click.stop="dismissNotification(item, 'NEW')">X</button>
			</div>
			<hr v-if="storedNotifications.length > 0" class="dropdown-divider m-0">
			</li>
			<li v-for="(item, index) in storedNotifications.slice().reverse()" :key="index">
				<div class="dropdown-item d-flex align-items-center me-2">
				{{ useI18n().t(`notif.${item.content}`) }}
				<button type="button" class="btn btn-sm btn-outline-dark ms-auto" aria-label="Close" @click.stop="dismissNotification(item, 'STORED')">X</button>
				</div>
			<hr v-if="index !== storedNotifications.length - 1" class="dropdown-divider m-0">
			</li>
		</ul>
	</div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';
import Backend from "../../js/Backend"
import Notifications from "../../js/Notifications"
import { ref } from 'vue'
import { watch, onMounted } from "vue"

let dropdownShown = ref(0);
const storedNotifications = ref([]);
const isLoaded = ref(false);
const idsToDeleteStored =ref([]);
const idsToDeleteNew =ref([]);

onMounted(() => {
  fetchData();
})

const fetchData = async () => {
	try {
		isLoaded.value = false;
		storedNotifications.value = await Backend.get('/api/users/me/notifications');
		// notifications.messages.value.push(NEW NOTIFICAITON);
		console.log(storedNotifications.value);
	} catch (err) {
		console.error(err.message);
	} finally {
		isLoaded.value = true;
	}
};

watch(() => Notifications.messages.value, () => {
	dropdownShown.value++;
});

function toggleDropdown() {
	dropdownShown.value = 0;
}

const dismissNotification = async(item, flag) => {
	try {
		await Backend.delete(`/api/users/me/notifications/${item.id}`);
		if(flag === 'STORED'){
			idsToDeleteStored.value.push(item.id);
			storedNotifications.value = storedNotifications.value.filter(item => !idsToDeleteStored.value.includes(item.id));
		}else if(flag === 'NEW') {
			idsToDeleteNew.value.push(item.id);
			Notifications.messages.value = Notifications.messages.value.filter(item => !idsToDeleteNew.value.includes(item.id));
		}
		dropdownShown.value--;
	} catch (err) {
		console.error(err.message);
	}
}
</script>

<style scoped>

.dropdown-menu {
	max-height: 196px;
	overflow-y: auto;
}

.dropdown-item:hover {
	background-color: lightgrey;
}
</style>
