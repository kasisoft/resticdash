import { ApplicationState } from "$lib/types";

function getItem(key: string): string | null {
    if (typeof localStorage === 'undefined') {
        return null;
    }
    return localStorage.getItem(key);
}

function setItem(key: string, value: string) {
    if (typeof localStorage !== 'undefined') {
        localStorage.setItem(key, value);
    }
}

function removeItem(key: string) {
    if (typeof localStorage !== 'undefined') {
        localStorage.removeItem(key);
    }
}

type Deserializer<T> = (input: string) => T | null | undefined;

function createStore<T>(key: string, defaultValue: T, deserializer: Deserializer<T> = JSON.parse) {

    const serializedStr: string | null = getItem(key);
    let serialized: T | null | undefined = null;
    if (serializedStr) {
        serialized = deserializer(serializedStr);
    }

    let result = $state(serialized || defaultValue);
    let changed = $state(false);
    
    function setValue(newValue: T) {
        if (newValue === undefined || newValue === null) {
            removeItem(key);
        } else {
            setItem(key, JSON.stringify(newValue));
        }
        changed = true;
        result = newValue;
    }

    function reset() {
        setValue(defaultValue);
        changed = false;
    }

    return {
        get value() { return result },
        get changed() { return changed },
        setValue,
        reset
    }

}

const applicationStateStore = createStore<ApplicationState>('applicationState', ApplicationState.Display);

export { applicationStateStore };
