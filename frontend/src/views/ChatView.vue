<script setup>
import { useI18n } from 'vue-i18n'
import { ref, onMounted } from 'vue'
import Backend from '../js/Backend'
import Chat from '../js/Chat'
import { globalUser } from '../main'
import Channel from '../components/chat/Channel.vue'
import Message from '../components/chat/Message.vue'
import GetAvatar from '../components/common/GetAvatar.vue'

const messageInput = ref('')
const targetNickname = ref('')

const blockedUsers = ref([])
const dmUserBlocked = ref(false)

const channelError = ref('')
const messageError = ref('')

onMounted(() => {
    loadChannels();
    loadBlockedUsers();
    Chat.messages.value = []
    Chat.selected_channel.value = null
})

async function loadChannels() {
    try {
        Chat.channels.value = []
        let data = await Backend.get('/api/users/me/channels')
        Chat.channels.value = data
    } catch (err) {
        channelError.value = err.message;
    }
}

async function loadBlockedUsers() {
    try {
        blockedUsers.value = []
        blockedUsers.value = await Backend.get(`/api/users/me/blocked`)
        console.log("Loaded blocked users")
    } catch (err) {
        console.error(err.message)
        // TODO: Display error message
    }
}

async function loadMessages(channel) {
    try {
        let data = await Backend.get(`/api/channels/${channel.id}/messages`)
        Chat.messages.value = data
        Chat.selected_channel.value = channel
    } catch (err) {
        console.error(err.message)
        Chat.messages.value = []
        // TODO: Display error message
    }
}

async function selectChannel(channel) {
    await loadMessages(channel)
    dmUserBlocked.value = await isDmUserBlocked()
}

async function createChannel() {
    try {
        let data = await Backend.post(`/api/channels`, {
            nickname: targetNickname.value
        })
        Chat.channels.value.unshift(data)
        channelError.value = ''
    } catch (err) {
        channelError.value = err.message;
    }
}

async function sendMessage() {
    let channel_id = Chat.selected_channel.value.id
    try {
        let data = await Backend.post(`/api/channels/${channel_id}/messages`, {
            content: messageInput.value
        })
        messageInput.value = '';
        messageError.value = ''
    } catch (err) {
        messageError.value = err.message
    }
}

async function deleteMessage(message) {
    try {
        await Backend.delete(`/api/messages/${message.id}`)
    } catch (err) {
        messageError.value = err.message
    }
}

async function inviteUser() {
    let channel_id = Chat.selected_channel.value.id
    try {
        await Backend.post(`/api/channels/${channel_id}/messages`, {
            content: "game-invite"
        })
    } catch (err) {
        messageError.value = err.message
    }
}

async function blockUser() {
    let dm_user = getChannelMember()

    try {
        await Backend.post(`/api/users/me/blocked`, {
            user_id: dm_user.id
        })
        blockedUsers.value.unshift(dm_user)
        dmUserBlocked.value = true
    } catch (err) {
        // TODO: Error handling
        console.error(`Failed to block: ${err.message}`)
    }

}

async function unblockUser() {
    let dm_user = getChannelMember()

    try {
        await Backend.delete(`/api/users/me/blocked/${dm_user.id}`, {
            user_id: dm_user.id
        })
        blockedUsers.value = blockedUsers.value.filter(u => u.id !== dm_user.id)
        dmUserBlocked.value = false
    } catch (err) {
        // TODO: Error handling
        console.error("Failed to unblock")
    }
}

async function isDmUserBlocked() {
    let dm_user = getChannelMember()

    return blockedUsers.value.some(e => e.id == dm_user.id)
}

function getChannelMember() {
    if (Chat.selected_channel.value.members[0].id === globalUser.value.id) {
        return Chat.selected_channel.value.members[1]
    }
    return Chat.selected_channel.value.members[0]
}
</script>

<template>
    <div class="boxstyling">
        <div class="box rounded">
            <div class="row">
                <!-- Sidebar with channels -->
                <div class="col">
                    <div class="mb-2">
                        <div class="input-group">
                            <input type="text" :placeholder="useI18n().t('chatview.nickname')" class="form-control"
                                v-model="targetNickname" @keyup.enter="createChannel" />
                            <button class="btn btn-primary"
                                @click="createChannel">{{ useI18n().t('chatview.create') }}</button>
                        </div>
                        <div v-if="channelError !== ''" class="alert alert-danger d-flex align-items-center p-1 mt-1"
                            role="alert">
                            {{ useI18n().te(`err.${channelError}`) ? useI18n().t(`err.${channelError}`) : channelError }}
                        </div>
                    </div>
                    <ul class="channel-container list-group">
                        <Channel v-for="channel in Chat.channels.value" :key="channel.id" :channel="channel"
                            :selected="channel === Chat.selected_channel.value" @selected="selectChannel(channel)" />
                    </ul>
                </div>

                <!-- Container for selected channels -->
                <div v-if="Chat.selected_channel.value" class="col-md-9">
                    <div class="border rounded d-flex align-items-center mb-1">
                        <GetAvatar :id="getChannelMember().id" :size=40 class="m-1 mr-2" />
                        <router-link class="message-author" :to="'/users/' + getChannelMember().id">{{
                                getChannelMember().username
                            }}</router-link>
                        <div class="input-group m-1 justify-content-end">
                            <button v-if="!dmUserBlocked" class="btn btn-primary"
                                @click="inviteUser">{{ useI18n().t('chatview.invite') }}</button>
                            <button v-if="!dmUserBlocked" class="btn btn-danger"
                                @click="blockUser">{{ useI18n().t('chatview.blockUser') }}</button>
                            <button v-else class="btn btn-success"
                                @click="unblockUser">{{ useI18n().t('chatview.unblockUser') }}</button>
                        </div>
                    </div>
                    <div class="message-container">
                        <Message v-for="message in Chat.messages.value" :key="message.id" :message="message"
                            @deleted="deleteMessage(message)" />
                    </div>
                    <div class="mt-2">
                        <div class="input-group mb-2">
                            <input type="text" class="form-control" v-model="messageInput" @keyup.enter="sendMessage"
                                :placeholder="useI18n().t('chatview.sendMessage')" />
                        </div>
                        <div v-if="messageError !== ''" class="alert alert-danger d-flex align-items-center p-1"
                            role="alert">
                            {{ useI18n().te(`err.${messageError}`) ? useI18n().t(`err.${messageError}`) : messageError}}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.channel-container {
    height: 70vh;
    overflow: auto;
    display: flex;
    flex: 0 0 auto;
}

.message-container {
    height: 70vh;
    overflow: auto;
    display: flex;
    flex: 0 0 auto;
    flex-direction: column-reverse;
}
</style>
