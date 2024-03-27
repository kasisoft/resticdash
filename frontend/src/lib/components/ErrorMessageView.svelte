<script lang="ts">

    import { Alert } from 'svelte-5-ui-lib';
    import { InfoCircleSolid } from 'flowbite-svelte-icons';

    import { alertStore } from '$lib/stores.svelte';
    import { _ } from 'svelte-i18n';

    function dismiss() {
        alertStore.reset();
    }

</script>

{#if alertStore.changed}
    <Alert divclass="border-t-4 border-b-4 full-width bg-red-50 text-red-800 border-red-600 border-y-2" dismissable onclick={dismiss}>
        {#snippet icon()}
            <InfoCircleSolid class="w-5 h-5" />
        {/snippet}
        <span class="font-medium">{$_('general.error')}:</span>{alertStore.value}
    </Alert>
{/if}
