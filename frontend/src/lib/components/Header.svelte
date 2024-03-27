<script lang="ts">

    import { Darkmode } from 'svelte-5-ui-lib';

    import ErrorMessageView from '$lib/components/ErrorMessageView.svelte';

</script>

<header class="full-width content-grid">
    <div class="flex flex-row justify-between">
        <h1 class="text-6xl">ResticDash</h1>
        <Darkmode btnclass="dark:bg-primary-900 hover:dark:bg-primary-900 bg-primary-300 hover:bg-primary-300"/>
    </div>
    <ErrorMessageView />
</header>


<style lang="postcss">
    header {
        grid-template-rows: var(--header-height) auto;
    }
</style>
