import { createSignal, For } from 'solid-js';
import ButtonNewChat from "./ButtonNewChat";

const Sidebar = (props) => {

    const [data] = createSignal(props.data);

    const handleClick = (item) => {
        localStorage.setItem('data', JSON.stringify(item));
        props.selectItem('')
        props.selectItem('historical')
   
    };

    return (
        <aside>
            <ButtonNewChat selectItem={props.selectItem} />
            <div class="space-y-2 m-2">
                <For each={data()}>{(item) =>
                    <button
                        id={item.address}
                        class="text-sm text-start space-y-2 bg-gray-600 px-2 rounded-sm w-full hover:opacity-90 h-8 text-white"
                        title={item.address}
                        onClick={() => handleClick(item)}

                    >
                        {item.address}
                    </button>
                }</For>
            </div>
        </aside>
    );
};

export default Sidebar;