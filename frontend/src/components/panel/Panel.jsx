import Form from "./Form";

import { createSignal } from 'solid-js';
import Aside from "./Aside";
import Historical from "./Historical";


const options = (param) => {
    switch (param) {
        case "form":
            return <Form />
        case "historical":
            return <Historical/>
        default:
            return null
    }
}

export default function Panel(props) {
    const [param, setParam] = createSignal('form');
    return (
        <div class="flex w-screen">
            <Aside data={props.data} selectItem={setParam} />

            <div class="w-full">
                {options(param())}
            </div>
        </div>
    )
}