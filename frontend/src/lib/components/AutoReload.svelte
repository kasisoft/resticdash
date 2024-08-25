<script lang="ts">

    import { Spinner } from 'svelte-5-ui-lib';

    import { ResticDashClient } from '$lib/client';
    import { ApplicationState } from '$lib/types';
    import { alertStore, applicationStateStore, backupinfosStore, configStore, progressStore } from '$lib/stores.svelte';

    import { _ } from 'svelte-i18n';

    let timeout: NodeJS.Timeout | null = null;

    async function loadRestic() {
        if (timeout) {
            clearInterval(timeout);
            timeout = null;
        }
        applicationStateStore.setValue(ApplicationState.Loading);
        progressStore.setValue(configStore.value.timeout);
        const progressTicker = setInterval(() => progressStore.setValue(progressStore.value - 1), 1000);
        const client = new ResticDashClient(configStore.value.timeout, alertStore.setValue, $_('general.connection_aborted'));
        const result = await client.getRestic();
        clearInterval(progressTicker);
        if (result !== undefined) {
            backupinfosStore.setValue(result);
        }
        applicationStateStore.setValue(ApplicationState.Display);
        timeout = setInterval(loadRestic, configStore.value.reload * 1000);
    }

    loadRestic();

</script>

<div class="full-width">
{#if applicationStateStore.value == ApplicationState.Display}
    <div class="progressbar">
        <div class="progress" style="animation-duration: {configStore.value.reload}s;"></div>
    </div>
{:else if applicationStateStore.value  == ApplicationState.Loading}
    <div role="status">
        <Spinner size={10} color="blue" bg="text-gray-300"/>
        &nbsp;&nbsp;{$_('loading.timeout')}&nbsp;{progressStore.value}s
    </div>
{/if}
</div>

<style lang="postcss">

    div {
        min-height: 3.5rem;
        max-height: 3.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        > div[role='status'] {
            justify-self: center;
        }
    }

    .progressbar {
        width: 100%;
        overflow: hidden;
        justify-content: flex-start;
    }

    .progress {
        height: 100%;
        width: 100%;
        background-color: theme('colors.primary.500');
        transition: width 1s ease-in-out;
        animation-timing-function: linear;
        animation-fill-mode: forwards;
        animation-name: reduceFill;
    }

    @keyframes reduceFill {
        from { width: 100%; }
        to { width: 0%; }
    }

</style>

