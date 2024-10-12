import {
    QueryClient,
    QueryClientProvider,
    createQuery,
    keepPreviousData,
} from '@tanstack/solid-query'
import { SolidQueryDevtools } from '@tanstack/solid-query-devtools'
import {
    For,
    Show,
    Suspense,
    createContext,
    useContext
} from 'solid-js'
import { isServer } from 'solid-js/web'
import { getSearchParams } from '../utils'
import PropertyForm from './Form'
import { Link } from './Link'


const PropertyIdContext = createContext<() => string>()

const usePropertyID = () => {
    const id = useContext(PropertyIdContext)
    if (!id) throw new Error('PropertyIdContext not found')
    return id
}





export const SolidApp = (props: { property?: string }) => {
    const client = new QueryClient()

    const search = getSearchParams(props.property || '')

    return (
        <QueryClientProvider client={client}>
            <SolidQueryDevtools />
            <Suspense fallback={'Loading'}>
                <PropertyIdContext.Provider value={search}>
                    <App />
                </PropertyIdContext.Provider>
            </Suspense>
        </QueryClientProvider>
    )
}

const App = () => {
    return (
        <div class="flex flex-1 overflow-auto h-[100vh]">
            <SideNav />
            <PropertyDetails />
        </div>
    )
}

const PropertyDetails = () => {
    const id = usePropertyID()
    console.log("id ", id())
    return (
        <div class="flex-1 flex">
            <Show when={id()}>
                <Suspense fallback={'Loading'}>
                    <PropertyCard id={id()} />
                </Suspense>
            </Show>
            <Show when={!id()}>
                <PropertyForm />
            </Show>
        </div>
    )
}

const PropertyCard = (props: { id: string }) => {
    const property = createQuery(() => ({
        queryKey: ['property', props.id],
        queryFn: async () => {
            const res = await fetch(
                `${import.meta.env.PUBLIC_API}/v1/predict/history/${props.id}`
            ).then((res) => res.json())
            return res
        },
        placeholderData: keepPreviousData,
    }))

    const is_server_rendered = createQuery(() => ({
        queryKey: ['is_server_rendered', props.id],
        queryFn: () => {
            if (isServer) return true
            return false
        },
        placeholderData: keepPreviousData,
    }))

    return (
        <div class="flex flex-col flex-1 items-center">
            <div class="flex justify-center py-4">
                <div>
                    <Show
                        when={is_server_rendered.data}
                        fallback={
                            <>
                                ...
                            </>
                        }
                    >
                        <b>server. </b>

                    </Show>
                </div>
            </div>
            <Show when={property.data}>
                <div class="max-w-md w-full bg-white shadow-lg rounded-lg overflow-hidden border border-slate-300">
                    <div class="p-6 space-y-6">
                        <div class="flex items-center justify-between border-b border-gray-200 pb-4">
                            <h2 class="text-2xl font-bold text-gray-800"> {property.data.city}, {property.data.state}</h2>
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-home-dollar w-6 h-6 text-blue-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <path d="M19 10l-7 -7l-9 9h2v7a2 2 0 0 0 2 2h6" />
                                <path d="M9 21v-6a2 2 0 0 1 2 -2h2c.387 0 .748 .11 1.054 .3" />
                                <path d="M21 15h-2.5a1.5 1.5 0 0 0 0 3h1a1.5 1.5 0 0 1 0 3h-2.5" />
                                <path d="M19 21v1m0 -8v1" />
                            </svg>

                        </div>

                        <div class="space-y-4">
                            <div class="flex items-center justify-between">
                                <span class="text-gray-600 font-medium">Address:</span>
                                <span class="text-gray-800 font-semibold">{property.data.address}</span>
                            </div>

                            <div class="flex items-center justify-between">
                                <span class="text-gray-600 font-medium flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-currency-dollar w-4 h-4 mr-1 text-green-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#00b341" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                        <path d="M16.7 8a3 3 0 0 0 -2.7 -2h-4a3 3 0 0 0 0 6h4a3 3 0 0 1 0 6h-4a3 3 0 0 1 -2.7 -2" />
                                        <path d="M12 3v3m0 12v3" />
                                    </svg>
                                    Price:
                                </span>
                                <span class="text-gray-800 font-semibold">${property.data.price.toLocaleString()}</span>
                            </div>

                            <div class="flex items-center justify-between bg-green-50 p-2 rounded-md">
                                <span class="text-green-700 font-medium flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-currency-dollar w-4 h-4 mr-1 text-green-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#00b341" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                        <path d="M16.7 8a3 3 0 0 0 -2.7 -2h-4a3 3 0 0 0 0 6h4a3 3 0 0 1 0 6h-4a3 3 0 0 1 -2.7 -2" />
                                        <path d="M12 3v3m0 12v3" />
                                    </svg>

                                    Predicted Price:
                                </span>
                                <span class="text-green-700 font-semibold">${property.data.predicted_price.toLocaleString()}</span>
                            </div>

                            <div class="grid grid-cols-2 gap-4">
                                <div class="flex items-center justify-between bg-gray-50 p-2 rounded-md">
                                    <span class="text-gray-600 font-medium flex items-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-bed-filled w-4 h-4 mr-1 text-blue-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                            <path d="M3 6a1 1 0 0 1 .993 .883l.007 .117v6h6v-5a1 1 0 0 1 .883 -.993l.117 -.007h8a3 3 0 0 1 2.995 2.824l.005 .176v8a1 1 0 0 1 -1.993 .117l-.007 -.117v-3h-16v3a1 1 0 0 1 -1.993 .117l-.007 -.117v-11a1 1 0 0 1 1 -1z" stroke-width="0" fill="currentColor" />
                                            <path d="M7 8a2 2 0 1 1 -1.995 2.15l-.005 -.15l.005 -.15a2 2 0 0 1 1.995 -1.85z" stroke-width="0" fill="currentColor" />
                                        </svg>
                                        Bedrooms:
                                    </span>
                                    <span class="text-gray-800 font-semibold">{property.data.bedrooms}</span>
                                </div>

                                <div class="flex items-center justify-between bg-gray-50 p-2 rounded-md">
                                    <span class="text-gray-600 font-medium flex items-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-bath w-4 h-4 mr-1 text-blue-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                            <path d="M4 12h16a1 1 0 0 1 1 1v3a4 4 0 0 1 -4 4h-10a4 4 0 0 1 -4 -4v-3a1 1 0 0 1 1 -1z" />
                                            <path d="M6 12v-7a2 2 0 0 1 2 -2h3v2.25" />
                                            <path d="M4 21l1 -1.5" />
                                            <path d="M20 21l-1 -1.5" />
                                        </svg>
                                        Bathrooms:
                                    </span>
                                    <span class="text-gray-800 font-semibold">{property.data.bathrooms}</span>
                                </div>
                            </div>

                            <div class="flex items-center justify-between bg-gray-50 p-2 rounded-md">
                                <span class="text-gray-600 font-medium flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-meter-square w-4 h-4 mr-1 text-blue-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                        <path d="M17 5h2a1 1 0 0 1 1 1v1a1 1 0 0 1 -1 1h-1a1 1 0 0 0 -1 1v1a1 1 0 0 0 1 1h2" />
                                        <path d="M4 12v6" />
                                        <path d="M4 14a2 2 0 0 1 2 -2h.5a2.5 2.5 0 0 1 2.5 2.5v3.5" />
                                        <path d="M9 15.5v-1a2.5 2.5 0 1 1 5 0v3.5" />
                                    </svg>

                                    Square Feet:
                                </span>
                                <span class="text-gray-800 font-semibold">{property.data.square_feet.toLocaleString()}</span>
                            </div>

                            <div class="flex items-center justify-between bg-gray-50 p-2 rounded-md">
                                <span class="text-gray-600 font-medium flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-calendar w-4 h-4 mr-1 text-blue-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                        <path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12z" />
                                        <path d="M16 3v4" />
                                        <path d="M8 3v4" />
                                        <path d="M4 11h16" />
                                        <path d="M11 15h1" />
                                        <path d="M12 15v3" />
                                    </svg>
                                    Year Built:
                                </span>
                                <span class="text-gray-800 font-semibold">{property.data.year_built}</span>
                            </div>
                            <div class="flex items-center justify-between bg-gray-50 p-2 rounded-md">
                                <span class="text-gray-600 font-medium flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-calendar w-4 h-4 mr-1 text-blue-600" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                        <path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12z" />
                                        <path d="M16 3v4" />
                                        <path d="M8 3v4" />
                                        <path d="M4 11h16" />
                                        <path d="M11 15h1" />
                                        <path d="M12 15v3" />
                                    </svg>
                                    Predition date
                                </span>
                                <span class="text-gray-800 font-semibold">{String(property.data.prediction_date).replace("T", " ").substring(0, 19)}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </Show>
        </div>
    )
}

const SideNav = () => {
    const id = usePropertyID()

    const chats = createQuery(() => ({
        queryKey: ['chats'],
        queryFn: async () => {
            const res = await fetch(`${import.meta.env.PUBLIC_API}/v1/predict/history`)
                .then(res => res.json());
            return res?.items || []
        },
        placeholderData: keepPreviousData,
    }));



    const activeClass = (propertyID: string) =>
        id() === propertyID ? 'bg-gray-50' : 'hover:bg-gray-50'
    interface NavItem {
        navigate: string;
        title: string;
    }



    return (
        <div class="w-72 border-r flex flex-col px-2">
            <div class="pt-3 pb-1 text-sm font-semibold flex w-full">
                <p class='grow'>Consultas</p>
                <button
                onclick={()=>window.location.href="./panel"} 
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-plus h-6 w-6 stroke-black" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                        <path d="M12 5l0 14" />
                        <path d="M5 12l14 0" />
                    </svg>
                </button>
            </div>

            <div class="flex-1 overflow-auto flex flex-col gap-1">
                <For each={chats.data}>
                    {(item) => (
                        <Link
                            class={`flex gap-2 items-center border border-slate-300 rounded p-1 ${activeClass(item.id)}`}
                            href={`./?id=${item.id}`}
                        >
                            <div class="flex flex-col">
                                <span class="text-sm font-semibold">
                                    {item.address}, {item.city}, {item.state}
                                </span>
                                <span class="text-xs text-zinc-600">
                                    {item.bedrooms} beds, {item.bathrooms} baths
                                </span>
                                <span class="text-xs text-zinc-600">
                                    Price: ${item.price.toLocaleString()} - Predicted: ${item.prediction.predicted_price.toLocaleString()}
                                </span>
                            </div>
                        </Link>
                    )}
                </For>
            </div>
        </div>
    );
}
