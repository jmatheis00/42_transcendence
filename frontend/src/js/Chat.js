import { ref } from 'vue';
import Backend from './Backend';
import Notifications from './Notifications';

class Chat {
    static messages = ref([])
    static channels = ref([])
    static selected_channel = ref(null)

    static async createMessage(event) {
        let url = window.location.pathname

        if (url.startsWith("/chat")) {
            let message = event.payload
            let channel_id = message.channel_id

            let selected_channel = Chat.selected_channel.value
            if (selected_channel && selected_channel.id == channel_id) {
                Chat.messages.value.unshift(event.payload)
            }

            // Update the channel's updated_at field
            let channel = Chat.channels.value.find(c => c.id === channel_id)
            channel.updated_at = event.payload.created_at

            // Move the channel to the top of the list
            Chat.channels.value = Chat.channels.value.filter(c => c.id !== channel_id)
            Chat.channels.value.unshift(channel)
        } else {
            await Notifications.post(event);
        }
    }

    static async deleteMessage(event) {
        let url = window.location.pathname

        if (url.startsWith("/chat")) {
            let message_id = event.payload.id
            Chat.messages.value = Chat.messages.value.filter(m => m.id !== message_id)
        }
    }
}

export default Chat