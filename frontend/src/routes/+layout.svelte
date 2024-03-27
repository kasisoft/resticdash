<script lang="ts">

    import '$src/styles.pcss';

    import { dictionary, getLocaleFromNavigator, getLocaleFromQueryString, init } from 'svelte-i18n';

    import Header from '$lib/components/Header.svelte';
    import Footer from '$lib/components/Footer.svelte';

    import { ResticDashClient } from '$lib/client';
    import { alertStore, configStore } from '$lib/stores.svelte';

    let { data } = $props();

    dictionary.set(data.dictionary);
    init({
        fallbackLocale: 'en',
        initialLocale: getLocaleFromQueryString('lang') ?? getLocaleFromNavigator(),
    });

    async function loadConfig() {
        const client = new ResticDashClient(configStore.value.timeout, alertStore.setValue);
        const result = await client.getConfig();
        if (result !== undefined) {
            configStore.setValue(result);
        }
    }

    loadConfig();

</script>

<div class="app content-grid">
    <Header />
    <main class="full-width content-grid">
        <slot />
    </main>
    <Footer />
</div>


<style lang="postcss">
    .app {
        min-height: 100vh;
        min-height: 100svh;
        display: grid;
        grid-template-rows: auto 1fr auto;
    }
    main {
        height: 100%;
        width: 100%;
        background-color: var(--color-light-background);
    }
</style>
