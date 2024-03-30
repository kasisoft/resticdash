import { ApplicationState, BackupInfosListDef, DEFAULT_FRONTENDCFG, FrontendCfgDef, type BackupInfosList, type FrontendCfg } from '$lib/types';
import type { CheckResult } from 'arktype/internal/traverse/traverse.js';

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
        if (newValue == undefined || newValue == null) {
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

function newObject<T>(obj: string, defVal: T, constructor: (value: any) => CheckResult<T>): T {
    const parsed = JSON.parse(obj);
    const result = constructor(parsed);
    if (result.problems) {
        console.error(`Error Input:\n${obj}`);
        console.error(JSON.stringify(result.problems));
        return defVal;
    }
    return result.data;
}

function buildBackupInfosList(input: string): BackupInfosList {
    return newObject<BackupInfosList>(input, [], BackupInfosListDef);
}

function buildFrontendCfgt(input: string): FrontendCfg {
    return newObject<FrontendCfg>(input, DEFAULT_FRONTENDCFG, FrontendCfgDef);
}

const alertStore = createStore<string>('alertState', '');
const applicationStateStore = createStore<ApplicationState>('applicationState', ApplicationState.Display);
const backupinfosStore = createStore<BackupInfosList>('backupInfos', [], buildBackupInfosList);
const configStore = createStore<FrontendCfg>('frontend', DEFAULT_FRONTENDCFG, buildFrontendCfgt);
const progressStore = createStore<number>('progress', DEFAULT_FRONTENDCFG.timeout);

export { alertStore, applicationStateStore, backupinfosStore, configStore, progressStore };
