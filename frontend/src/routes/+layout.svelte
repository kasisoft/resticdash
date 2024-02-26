<script lang="ts">

    import '$src/styles.pcss';
    import { dictionary, getLocaleFromNavigator, getLocaleFromQueryString, init } from 'svelte-i18n';

    import ErrorMessageView from '$lib/components/ErrorMessageView.svelte';
    import Header from '$lib/components/Header.svelte';
    import Footer from '$lib/components/Footer.svelte';
    
    import { ResticDashClient } from '$lib/client';
    import { alertStore, configStore } from '$lib/stores.svelte';

    export let data;

    dictionary.set(data.dictionary);

    let lang = getLocaleFromQueryString('lang');
    if (!lang) {
        lang = getLocaleFromNavigator();
    }

    init({
        fallbackLocale: 'en',
        initialLocale: lang, 
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
    <header class="full-width content-grid">
        <Header />
        <ErrorMessageView />
    </header>
    <main class="full-width content-grid">
        <slot />
    </main>
    <footer class="full-width content-grid">
        <Footer />
    </footer>
</div>


<style lang="postcss">
    .app {
        min-height: 100vh;
        min-height: 100svh;
        display: grid;
        grid-template-rows: auto 1fr auto;
    }
    header {
        grid-template-rows: var(--header-height) auto;
        background-color: theme('colors.primary.300');
    }
    main {
        height: 100%;
        width: 100%;
        background-color: theme('colors.primary.100');
    }
    footer {
        background-color: theme('colors.primary.300');
    }
</style>
