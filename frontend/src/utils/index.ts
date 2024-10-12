import { createSignal, createEffect } from 'solid-js'
import type { Accessor, Setter } from 'solid-js'

export const getSearchParams = (init: string): [Accessor<string>, Setter<string>] => {
    const [search, setSearch] = createSignal(init)

    if (typeof window !== 'undefined') {
        createEffect(() => {
            const updateSearch = () => {
                const params = new URLSearchParams(window.location.search)
                setSearch(params.get('id') || '')
            }

            window.addEventListener('popstate', updateSearch)
            updateSearch()

            return () => window.removeEventListener('popstate', updateSearch)
        })
    }

    return [search, setSearch]
}

export const properCase = (str: string) =>
    str.charAt(0).toUpperCase() + str.slice(1)