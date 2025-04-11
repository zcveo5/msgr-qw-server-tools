import hashlib
import tkinter
import shutil
import socket
import threading
from tkinter import ttk
from tkinter.messagebox import showinfo as t_showinfo, askyesno, showwarning
from plugins.core.mod import *
import plugins.btac.auth
auth = plugins.btac.auth

printr = print


# init classes and functions


def shutdown():
    main.destroy()


def plugin_info():
    _show('BTAEML (BebraTech Application Engine Mod Loader)', "BTAEML (BebraTech Application Engine Mod Loader) coded by BebraTech Inc. (BTAE authors).\n"
                                         "ALL plugins/mods made by other people (not BebraTech Inc.)\n"
                                         "We aren't take responsibility if your PC damaged by plugins/mods.\n\n"
                                         "BTAEML is included in all BTAE version 2.8.9 and above.\n"
                                         "In other versions BTAEML work unstable.\n\n"
                                         "BTAEML Team (BebraTech subdivision) 2025")



def _show(title, text, ret_win=False, custom_close=None):
    global last_obj_id
    obj_id = f'{text}{text}{ret_win}{custom_close}'
    info = Tk()
    def exit_mb():
        nonlocal info
        info.destroy()
        info = None
        if custom_close is not None:
            custom_close()
    info.title(title)
    try:
        fnt = font_theme
        bg = default_bg
        fg = default_fg
        info.configure(bg=bg)
    except NameError:
        fnt = ('Consolas', 9)
        bg = 'white'
        fg = 'black'
        info.configure(bg=bg)
    info.resizable(False, False)
    Label(info, text=text, bg=bg, fg=fg, font=fnt, justify=LEFT).pack(anchor='center', pady=30, ipadx=10)
    Button(info, text='OK', bg=bg, fg=fg, font=fnt, command=exit_mb).pack(anchor='se', side='bottom', expand=True, ipadx=10, ipady=5)
    if last_obj_id == '':
        last_obj_id = obj_id
    if ret_win:
        return info


class Settings:
    def __init__(self):
        self.window_other = None
        self.window_debug = None
        self.d_b = None
        self.window_locale = None
        self.window_theme = None
        self.br = Button
        self.test1 = Button
        self.test2 = Button
        self.l_th_b = Button
        self.theme_button = Button
        self.th_file = Entry
        self.advanced = None
        global default_bg, default_fg
        self.theme = data['USER_SETTINGS']['THEME']
        self.window = Tk()
        self.window.configure(bg=default_bg)
        self.window.title(locale['settings_mm_butt'])
        self.window.resizable(False, False)
        self.window.geometry('200x200')
        Button(self.window, text=locale['setting_sub_f_THEME'], command=self.sub_f_theme
               , fg=default_fg, bg=default_bg, font=font_theme).pack(anchor='nw')
        Button(self.window, text=locale['setting_sub_f_LOCALE'], command=self.sub_f_locale
               , fg=default_fg, bg=default_bg, font=font_theme).pack(anchor='nw')
        Button(self.window, text=locale['setting_sub_f_DEBUG'], command=self.sub_f_debug
               , fg=default_fg, bg=default_bg, font=font_theme).pack(anchor='nw')
        Button(self.window, text=locale['setting_sub_f_OTHER'], command=self.sub_f_other
               , fg=default_fg, bg=default_bg, font=font_theme).pack(anchor='nw')
        Button(self.window, text=locale['as_button'], command=self.advanced_settings, bg=default_bg,
               fg=default_fg, font=font_theme).pack(anchor='nw')
        Button(self.window, text=locale['setting_sub_f_PROFILE'], command=self.sub_f_profile, bg=default_bg,
               fg=default_fg, font=font_theme).pack(anchor='nw')
        Button(self.window, text=locale['setting_sub_f_MODS_REPO'], command=self.sub_f_mod_rep, bg=default_bg,
               fg=default_fg, font=font_theme).pack(anchor='nw')

    def advanced_settings(self):
        as_win = Tk()
        as_win.resizable(False, False)
        as_win.geometry('650x360')
        as_win.title(locale['as_button'])
        as_win.configure(bg=default_bg)
        try:
            sab = eval(dat_d['[SETTINGS]'])['ADV_DATA']
        except (json.decoder.JSONDecodeError, KeyError):
            Label(as_win, text=locale['damaged_data'], bg=default_bg, fg=default_fg, font=font_theme).pack(anchor='center')
            return
        try:
            self.advanced = Listbox(as_win, selectmode=SINGLE, width=100, height=20, bg=default_bg, fg=default_fg, font=font_theme)
            self.advanced.place(x=0, y=0)
            for item1 in sab:
                self.advanced.insert(0, item1)
            Button(as_win, text=locale['run_asb'], command=self.run_asb, bg=default_bg, fg=default_fg, font=font_theme).place(x=0, y=330)
        except Exception as _e123x:
            showerror('err', f'{_e123x}')

    def toggle_theme(self):
        global default_fg, default_bg
        if self.theme == 'light':
            self.theme = 'black'
            data['USER_SETTINGS']['THEME'] = self.theme
            default_bg = 'black'
            default_fg = 'white'
            refresh()
        elif self.theme == 'black':
            self.theme = 'light'
            data['USER_SETTINGS']['THEME'] = self.theme
            default_fg = 'black'
            default_bg = 'white'
            refresh()

    def run_asb(self):
        sab1 = eval(dat_d['[SETTINGS]'])
        try:
            exec(sab1['ADV_DATA'][self.advanced.get(self.advanced.curselection())])
        except AttributeError as adv_ex:
            showwarning(locale['warn_title'], locale['mod_error'] + str(adv_ex))
        except NameError:
            showerror(locale['error_title'], locale['damaged_data'])
        except ModuleNotFoundError:
            showwarning(locale['warn_title'], locale['mod_error'])
        except TclError:
            pass

    def sub_f_theme(self):
        self.window_theme = Tk()
        self.window_theme.configure(bg=default_bg)
        self.window_theme.title(locale['setting_sub_f_THEME'])
        self.window_theme.resizable(False, False)
        self.window_theme.geometry('200x200')
        Label(self.window_theme, text=locale['set_theme_txt'], fg=default_fg, bg=default_bg, font=font_theme).pack(anchor='nw', padx=3)
        longs = os.listdir('./data/theme')
        self.d_b = ttk.Combobox(self.window_theme, values=longs, state="readonly")
        self.d_b.bind("<<ComboboxSelected>>", self.sel_t)
        self.d_b.pack(anchor='nw', padx=3)
        Button(self.window_theme, text=locale['cct_title'], command=create_custom_theme, bg=default_bg, fg=default_fg, font=font_theme).pack(anchor='nw', padx=3)

    def sel_t(self, event):
        theme(self.d_b.get())
        user_local_settings['USER_SETTINGS']['THEME'] = self.d_b.get()
        reinit_window()

    def sub_f_locale(self):
        self.window_locale = Tk()
        self.window_locale.configure(bg=default_bg)
        self.window_locale.title(locale['setting_sub_f_LOCALE'])
        self.window_locale.resizable(False, False)
        self.window_locale.geometry('200x200')
        longs = os.listdir('./data/locale')
        Label(self.window_locale, text=locale['set_locale_txt'], fg=default_fg, bg=default_bg, font=font_theme).pack(anchor='nw', padx=3)
        self.d_b = ttk.Combobox(self.window_locale ,values=longs, state="readonly")
        self.d_b.bind("<<ComboboxSelected>>", self.set_l)
        self.d_b.pack(anchor='nw', padx=3)

    def set_l(self, event):
        global lng
        lng = self.d_b.get()
        user_local_settings['USER_SETTINGS']['SEL_LOCALE'] = self.d_b.get()
        refresh_locale()

    @staticmethod
    def sub_f_debug():
        try:
            debugtools()
        except Exception as db_open_error:
            _show('Error', f'Debug open error:\n{db_open_error}')

    @staticmethod
    def sub_f_profile():
        window_prof = Tk()
        window_prof.configure(bg=default_bg)
        window_prof.title(locale['setting_sub_f_PROFILE'])
        window_prof.resizable(False, False)
        window_prof.geometry('200x200')
        Label(window_prof, text=f"{locale['curr_acc']}: {username}", bg=default_bg, fg=default_fg,
               font=font_theme).pack(anchor='nw', padx=3)
        Button(window_prof, text=locale['un_login'], command=exit_acc, bg=default_bg, fg=default_fg,
               font=font_theme).pack(anchor='nw', padx=3)
        Button(window_prof, text=locale['public_ip'], command=p_ip_check, bg=default_bg, fg=default_fg, font=font_theme).pack(anchor='nw', padx=3)



    def sub_f_other(self):
        self.window_other = Tk()
        self.window_other.configure(bg=default_bg)
        self.window_other.title(locale['setting_sub_f_OTHER'])
        self.window_other.resizable(False, False)
        self.window_other.geometry('200x200')
        try:
            eval(user_local_settings['USER_SETTINGS']['TELEMETRY_ENABLED'])
        except Exception as exex:
            Label(self.window_other, text=f'DATA.NC damaged, {exex}', bg=default_bg, fg=default_fg, font=font_theme).pack()
            return
        if user_local_settings['USER_SETTINGS']['TELEMETRY_ENABLED'] == 'True':
            tm_text = locale['telemetry_button_enabled']
        else:
            tm_text = locale['telemetry_button_disabled']
        teem_button = Button(self.window_other, text=tm_text, command=lambda: telemetry_check(teem_button), bg=default_bg, fg=default_fg, font=font_theme)
        teem_button.pack(anchor='nw', padx=3)
        Button(self.window_other, text='cut BTAEML', command=cut_mod,
                                bg=default_bg, fg=default_fg, font=font_theme).pack(anchor='nw', padx=3)
        Button(self.window_other, text='LowLevel Update', command=upd_ll ,
               bg=default_bg, fg=default_fg, font=font_theme).pack(anchor='nw', padx=3)

    @staticmethod
    def sub_f_mod_rep():
        def get_mod_info(event):
            try:
                name_mod['text'] = mods_select.get(mods_select.curselection())
            except TclError:
                return
            try:
                name_mod['text'] += f'\n{_plugin_objects[mods_select.get(mods_select.curselection())]["metadata"]["description"]}'
                if mods_select.get(mods_select.curselection()) not in _plugin_objects:
                    name_mod['text'] += '\nThis plugin failed to load'
                    state_pl['text'] = 'Not loaded, installed'
                else:
                    state_pl['text'] = 'Loaded, installed'
            except:
                if mods_select.get(mods_select.curselection()) in _plugin_objects:
                    state_pl['text'] = 'Loaded, installed'
                    name_mod['text'] += '\nFailed to fetch plugin description'
                else:
                    name_mod['text'] += '\nThis plugin failed to load / not downloaded'
                    if mods_select.get(mods_select.curselection()) not in _plugin_objects:
                        state_pl['text'] = 'Not loaded, '
                    else:
                        state_pl['text'] = 'Loaded, '
                    if mods_select.get(mods_select.curselection()) not in installed_var.get():
                        state_pl['text'] += 'not installed'
                    else:
                        state_pl['text'] += 'installed'
            if mods_select.get(mods_select.curselection()) in ['core', 'backup', 'btac']:
                action_butt['state'] = DISABLED
            else:
                action_butt['state'] = NORMAL
        def install_mod():
            try:
                mods_select.get(mods_select.curselection())
            except TclError:
                return
            mod_data = auth.raw_request({'action': f'get_mod:{mods_select.get(mods_select.curselection())}'})
            down_mod = str(mod_data['answer'])
            print(down_mod)
            down_mod = down_mod.replace('&@', '\n')
            mod = SNConfig(down_mod).load()
            print(mod)
            compiled = {'meta': eval(mod['meta']), 'code': mod['code']}
            print(compiled)
            try:
                os.mkdir(f'./plugins/{compiled["meta"]["name"]}')
            except FileExistsError:
                pass
            with open(f'./plugins/{compiled["meta"]["name"]}/metadata.json', 'w'):
                pass
            with open(f'./plugins/{compiled["meta"]["name"]}/{compiled["meta"]["file"]}.py', 'w'):
                pass
            json.dump(compiled['meta'], JsonObject(open(f'./plugins/{compiled["meta"]["name"]}/metadata.json', 'w')))
            open(f'./plugins/{compiled["meta"]["name"]}/{compiled["meta"]["file"]}.py', 'w').write(compiled['code'].replace('%TAB', '	'))
        def remove_mod():
            nonlocal installed_var
            shutil.rmtree(f'./plugins/{mods_select.get(mods_select.curselection())}', ignore_errors=True)
            installed_var = Variable(modl_win, os.listdir('./plugins'))
        def load_repo():
            mods_select.configure(listvariable=mods_var)
            action_butt.configure(text='Install', command=install_mod)
        def load_installed():
            nonlocal installed_var
            installed_var = Variable(modl_win, os.listdir('./plugins'))
            mods_select.configure(listvariable=installed_var)
            action_butt.configure(text='Remove', command=remove_mod)

        modl_win = Tk()
        modl_win.title('Plugins Repository')
        modl_win.configure(bg=default_bg)
        modlist = eval(user.get_modlist()['answer'])
        Button(modl_win, text='Repository', command=load_repo, bg=default_bg, fg=default_fg, font=font_theme).place(x=0, y=0)
        Button(modl_win, text='Installed', command=load_installed, bg=default_bg, fg=default_fg, font=font_theme).place(x=100, y=0)
        mods_var = Variable(modl_win, modlist)
        installed_var = Variable(modl_win, os.listdir('./plugins'))
        mods_select = Listbox(modl_win, width=70, height=30, listvariable=installed_var, bg=default_bg, fg=default_fg, font=font_theme)
        mods_select.place(x=0, y=30)
        mods_select.bind('<<ListboxSelect>>', get_mod_info)
        action_butt = Button(modl_win, text='Install', command=install_mod, bg=default_bg, fg=default_fg, font=font_theme)
        action_butt.place(x=500, y=30)
        state_pl = Label(modl_win, text='', bg=default_bg, fg=default_fg, font=font_theme)
        state_pl.place(x=580, y=30)
        load_installed()
        name_mod = Label(modl_win, text='', bg=default_bg, fg=default_fg, font=font_theme, justify=LEFT)
        name_mod.place(x=500, y=60)
        modl_win.geometry('900x500')
        modl_win.resizable(False, False)

def upd_ll():
    base_conf['RUNT_ACTION'] = 'LL_Update'


def exit_acc():
    user_local_settings['USER_SETTINGS']['USERNAME'] = ''
    user_local_settings['USER_SETTINGS']['PASSWORD'] = ''
    _show('Info', 'Restart is required to exit your account')


def cut_mod():
    if askyesno('confirmation', 'do you really want to disable BTAEML?'):
        user_local_settings['USER_SETTINGS']['BTAEML'] = 'False'
        _show('ok', 'ok')


def ver_check(b):
    if 'dev' not in version:
        user_local_settings['USER_SETTINGS']['VER_BACKUP_ENABLED'] = 'False'
        _show(locale['inf_t'], locale['dev_warning'])
        return
    if user_local_settings['USER_SETTINGS']['VER_BACKUP_ENABLED'] == 'True':
        b.configure(text=locale['v_backup_button_disabled'])
        user_local_settings['USER_SETTINGS']['VER_BACKUP_ENABLED'] = 'False'
    else:
        b.configure(text=locale['v_backup_button_enabled'])
        user_local_settings['USER_SETTINGS']['VER_BACKUP_ENABLED'] = 'True'


def p_ip_check():
    global bt_server_data
    try:
        if bt_server_data[1]['answer']['_show_ip'] == 'True':
            auth.update_personal_conf(username, ['_show_ip', 'False'])
            _show('inf', locale['p-ip-disabled'])
        else:
            auth.update_personal_conf(username, ['_show_ip', 'True'])
            _show('inf', locale['p-ip-enabled'])
        bt_server_data = user.get_data()
    except ConnectionResetError:
        _show('Error', 'An existing connection was forcibly closed by the remote host\nBebraTech Server currently unavailable.')
    except TypeError:
        _show('Error', 'TypeError')


def telemetry_check(b):
    if user_local_settings['USER_SETTINGS']['TELEMETRY_ENABLED'] == 'True':
        b.configure(text=locale['telemetry_button_disabled'])
        user_local_settings['USER_SETTINGS']['TELEMETRY_ENABLED'] = 'False'
    else:
        b.configure(text=locale['telemetry_button_enabled'])
        user_local_settings['USER_SETTINGS']['TELEMETRY_ENABLED'] = 'True'


def theme(file2, ret=False):
    global default_fg, default_bg, font_theme
    file1 = f"./data/theme/{file2.replace('.theme', '')}.theme"
    try:
        theme_ = load(open(file1, 'r', encoding=encoding), default_bg, default_fg, font_theme)
    except FileNotFoundError:
        showerror(locale['error_title'], locale['theme_error'] + ' FileNotFound')
        return
    except IndexError:
        showerror(locale['error_title'], locale['theme_error'] + ' Index')
        return
    except LookupError:
        showerror(locale['error_title'], locale['theme_error'] + ' LookUp')
        return

    try:
        main.configure(bg=theme_[0])
    except TclError:
        showerror(locale['error_title'], locale['theme_error'] + ' Tcl')
        return
    font_theme = theme_[2]
    default_fg = theme_[1]
    default_bg = theme_[0]
    data['USER_SETTINGS']['THEME'] = file2.replace('.theme', '')
    if ret:
        return font_theme, default_fg, default_bg


def refresh1():
    reinit_ui()


def debugtools():
    debugger = Tk()
    debugger.title('DEBUG-TOOLS')
    debugger.resizable(False, False)
    cmd = Text(debugger)
    cmd.grid(column=0, row=1, columnspan=1, rowspan=100)
    ttk.Button(debugger, text='sys argv',
               command=lambda: _show('inf', str(sys.argv))).grid(column=1, row=4)
    ttk.Button(debugger, text='reset theme',
               command=lambda: theme_reset()).grid(column=1, row=5)
    ttk.Button(debugger, text='locals',
               command=lambda: _show('inf', str(locals()))).grid(column=1, row=6)
    ttk.Button(debugger, text='globals',
               command=lambda: _show('inf', str(globals()))).grid(column=1, row=7)
    ttk.Button(debugger, text='from globals',
            command=lambda: _show('inf', globals()[cmd.get("0.0", "end")])).grid(column=1, row=8)
    ttk.Button(debugger, text='ref locale',
               command=lambda: refresh_locale()).grid(column=1, row=11)
    var = BooleanVar()
    var.set(True)
    use_exec_hook = ttk.Button(debugger, text='!exh', command=lambda: exc_hook_execute(use_exec_hook, var))
    use_exec_hook.grid(column=0, row=0)
    ttk.Button(debugger, text='EXECUTE',
               command=lambda: execute(cmd.get("0.0", "end"), cmd, var.get())).grid(column=1, row=40)
    ttk.Button(debugger, text='logs',
               command=lambda: _show('log', open('./data/log.log', 'r').read())).grid(column=1, row=15)
    ttk.Button(debugger, text='bt data',
               command=lambda: _show('inf', f'DATA\n{bt_server_data}\nUSER\n{username}')).grid(column=1, row=19)
    ttk.Button(debugger, text='re login',
               command=lambda: relog()).grid(column=1, row=21)
    ttk.Button(debugger, text='set enc',
               command=lambda: change_enc(cmd.get("0.0", "end"))).grid(column=1, row=16)
    ttk.Button(debugger, text='set locale',
               command=lambda: change_lng(cmd.get("0.0", "end"))).grid(column=1, row=17)
    ttk.Button(debugger, text='reinit m win', command=reinit_window).grid(column=1, row=18)
    ttk.Button(debugger, text='data.nc editor', command=data_nc_editor).grid(column=1, row=20)
    ttk.Button(debugger, text='plugin create', command=plug_create).grid(column=1, row=22)
    ttk.Button(debugger, text='info', command=lambda: _show('inf', f'ver: {version}'
                         f'\nroute to executable file: {__file__}'
                         f'\nfile name: {__name__}'
                         f'\napp enc: {encoding}'
                         f'\nac: ')).grid(column=1, row=39)
    debugger.protocol("WM_DELETE_WINDOW", lambda: close_debug(debugger, cmd))
    debugger.mainloop()


def plug_create():
    def compile_plug():
        metadata = {'name': name_plug.get(), 'file': 'mod', 'class': class_plug.get(), 'state': 'True'}
        raw_code = code.get("0.0", END)

        code_v = f"#Start\n{raw_code.replace('    ', '%TAB').replace('	', '%TAB')}\n#End"
        dist = {'meta': str(metadata), 'code': code_v}

        conf = SNConfig('').dump(dist).replace('\n', '&@')
        code.insert(END, f'\n\nResult:\n{conf}')

    def upload_plug():
        metadata = {'name': name_plug.get(), 'file': 'mod', 'class': class_plug.get(), 'state': 'True'}
        raw_code = code.get("0.0", END)

        code_v = f"#Start\n{raw_code.replace('    ', '%TAB').replace('	', '%TAB')}\n#End"
        dist = {'meta': str(metadata), 'code': code_v}

        conf = SNConfig('').dump(dist).replace('\n', '&@')

        answer = auth.raw_request({'action': 'upload_mod', 'MOD_NAME': metadata['name'], 'PLUG_CODE': conf})
        if answer['answer'] == 'uploaded':
            _show('Info', 'Uploaded')
        else:
            _show('Error', 'Not Uploaded')

    def decompile():
        path = f'{name_plug.get()}'
        meta = f'./plugins/{path}/metadata.json'
        meta_decoded = json.load(open(meta, 'r'))
        code_path = f"./plugins/{path}/{meta_decoded['file']}.py"
        code.delete("0.0", END)
        code.insert("0.0", open(code_path, 'r', encoding='windows-1251').read())
        name_plug.delete("0", END)
        class_plug.delete("0", END)
        name_plug.insert("0", meta_decoded['name'])
        class_plug.insert("0", meta_decoded['class'])

    def save_plug():
        conf = SNConfig('').dump({'code': code.get("0.0", END), 'class': class_plug.get(), 'name': name_plug.get()}).replace('\n', '&@').replace('    ', '%TAB').replace('	', '%TAB')
        try:
            os.mkdir('./plugins/backup')
        except FileExistsError:
            pass
        with open(f'./plugins/backup/{name_plug.get()}.plug', 'w'):
            pass
        open(f'./plugins/backup/{name_plug.get()}.plug', 'w').write(conf)

    def open_plug():
        code.delete("0.0", END)
        class_plug.delete("0", END)
        plug = open(f'./plugins/backup/{name_plug.get()}.plug').read().replace('&@', '\n').replace('%TAB', '    ')
        name_plug.delete("0", END)
        conf_plug = SNConfig(plug).load()
        print(conf_plug)
        code.insert("0.0", conf_plug['code'])
        name_plug.insert("0", conf_plug['name'])
        class_plug.insert("0", conf_plug['class'])


    win = Tk()
    win.title('Plugin Create')
    win.resizable(False, False)
    name_plug = Entry(win)
    name_plug.insert("0", "Enter plugin name")
    name_plug.grid(column=0, row=0)
    class_plug = Entry(win)
    class_plug.insert("0", "Enter plugin main_class")
    class_plug.grid(column=0, row=1)
    code = Text(win)
    code.grid(column=1, row=0, rowspan=10, columnspan=2)
    Button(win, text='Compile', command=compile_plug).grid(column=1, row=11)
    Button(win, text='Compile & Upload', command=upload_plug).grid(column=1, row=12)
    Button(win, text='Open Compiled', command=decompile).grid(column=2, row=13)
    Button(win, text='Open .plug', command=open_plug).grid(column=2, row=11)
    Button(win, text='Save .plug', command=save_plug).grid(column=2, row=12)


def data_nc_editor():
    def save():
        with open('./data/DATA.NC', 'w', encoding='windows-1251') as nc_file:
             nc_file.write(encrypt(txt.get("0.0", END), eval(cc)))

    def load():
        txt.delete("0.0", END)
        txt.insert("0.0", decrypt(open('./data/DATA.NC', 'r').read(), eval(cc)))
    try:
        cc = base_conf['CC']
        editor_win = Tk()
        txt = Text(editor_win)
        txt.grid(column=0, row=0, columnspan=2)
        Button(editor_win, text='Save', command=save).grid(column=0, row=1)
        Button(editor_win, text='Load', command=load).grid(column=1, row=1)
    except Exception as editor_open_err:
        showerror('Error', f'Editor open error. {type(editor_open_err)}')


def exc_hook_execute(b: Button, v):
    v.set(not v.get())
    if v.get():
        b.configure(text='!exh')
    else:
        b.configure(text='exh')


def execute(code, cmd, use_exc_hook=False):
    cmd_win = Tk()
    out = Text(cmd_win)
    out.pack()
    out.insert('0.0', '=====EXECUTE LOG=====\n')
    cmd_win.bind("<FocusOut>", lambda x: cmd_win.destroy())
    if use_exc_hook:
        code_ = (f""
            f"import tkinter.messagebox\n"
            f"from tkinter import *\n"
            f"def pp(v):\n"
            f"   cmd.insert(END, v)\n"
            f"print = pp\n"
            f"{code.replace('	', '    ')}\n")
    else:
        code_ = code
        if 'drop' in code_.lower() or 'while True' in code_.lower():
            raise SyntaxError('policy error')
        def exec__():
            try:
                exec(code_, globals().update({'cmd': out}), locals())
            except Exception as ex:
                out.insert(END, traceback.format_exc())
                showinfo('Execution Error', str(ex))
        threading.Thread(target=exec__, args=()).start()
        out.insert(END, '\nProcess exited\n')



def relog():
    global bt_server_data
    bt_server_data = user.get_data()
    try:
        if bt_server_data['status'] == 'error':
            _show('Error', f'{bt_server_data}')
    except TypeError:
        pass


def close_debug(win, txt):
    try:
        txt.pack_forget()
    except tkinter.TclError:
        pass
    win.destroy()


def reinit_window():
    global main, chat_window, font_theme
    main.destroy()
    main = None
    main = Tk()
    main.geometry('900x500')
    main.resizable(False, False)
    main.title(locale['WINDOW_TITLE_TEXT'])
    chat_window = Text(main, fg=default_fg, bg=default_bg, font=font_theme, width=110)
    chat_window.place(x=0, y=0)
    refresh()


def change_lng(a):
    global lng
    lng = a
    user_local_settings['USER_SETTINGS']['SEL_LOCALE'] = a


def refresh_locale_easy(a, ret=False):
    global lng
    lng = a
    user_local_settings['USER_SETTINGS']['SEL_LOCALE'] = a
    encoding_l = 'utf-8'
    if lng != 'en':
        encoding_l = 'windows-1251'
    locale_fl1 = Config(f'./data/locale/{lng}/locale.cfg', coding=encoding_l)
    locale1 = Locale(locale_fl1)
    if ret:
        return locale1


def theme_easy(a, ret=False):
    data['USER_SETTINGS']['THEME'] = a
    if ret:
        try:
            theme_ = load(open(f'./data/theme/{a}.theme', 'r', encoding=encoding))
            return theme_[2], theme_[1], theme_[0]
        except Exception as theme_easy_ex:
            print(theme_easy_ex)


def change_enc(a):
    global encoding
    encoding = a


def refresh_locale():
    global locale, locale_fl, encoding
    try:
        locale_fl = Config(f'./data/locale/{lng}/locale.cfg', coding=encoding)
        locale = Locale(locale_fl)
        for _ in range(0, 5):
            refresh()
        reinit_window()
    except UnicodeDecodeError:
        if encoding == 'utf-8':
            encoding = 'windows-1251'
        else:
            encoding = 'utf-8'
        try:
            locale_fl = Config(f'./data/locale/{lng}/locale.cfg', coding=encoding)
            locale = Locale(locale_fl)
            for _ in range(0, 5):
                refresh()
            reinit_window()
        except (UnicodeDecodeError, LookupError, OSError):
            if encoding == 'utf-8':
                encoding = 'windows-1251'
            else:
                encoding = 'utf-8'
            try:
                locale_fl = Config(f'./data/locale/{lng}/locale.cfg', coding=encoding)
                locale = Locale(locale_fl)
                for _ in range(0, 5):
                    refresh()
                reinit_window()
            except (UnicodeDecodeError, LookupError, OSError):
                showerror(locale['error_title'], locale['uns_locale'])
    except LookupError:
        showerror(locale['error_title'], locale['encoding_error'])
    except OSError:
        showerror(locale['error_title'], locale['unk_error'])


def theme_reset():
    global default_fg, default_bg
    data['USER_SETTINGS']['THEME'] = 'black'
    default_bg = 'black'
    default_fg = 'white'
    main.configure(bg=default_bg)


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_window.insert(END, message + '\n\n')
        except Exception as conn_err:
            print(conn_err)
            showerror('recv_error', 'An existing connection with CHAT_SERVER was forcibly closed by the Host.')
            client_socket.close()
            break

def send_message(event=None):
    to_send = {'text': send_entry.get(), '_show_ip': bt_server_data[1]['answer']['_show_ip'], 'name': username}
    message = f"""{to_send}"""
    my_message.set("")
    try:
        client_socket.send(message.encode('utf-8'))
    except OSError:
        showerror('Error', 'SOCK_DISCONNECTED')
        to_send['text'] += ' (!) SOCK_DISCONNECTED'
    chat_window.insert(END, f"You: {to_send['text']}" + '\n\n')
    send_entry.delete("0", END)


def reinit_ui():
    global default_fg, default_bg, send_entry, chat_window
    if bt_server_data[1] == 'blocked':
        chat_window.place_forget()
        Label(text='You are blocked in BebraTech network').pack()
        Button(text='Exit from account', command=exit_acc).pack()
        return

    Button(text=locale['settings_mm_butt'], command=Settings, bg=default_bg, fg=default_fg, font=font_theme).place(x=800, y=5)

    update = Button(text=locale['refresh_butt'], command=refresh, bg=default_bg, fg=default_fg, font=font_theme)
    update.place(x=520, y=450)

    send_entry = Entry(width=110, bg=default_bg, fg=default_fg, font=font_theme, textvariable=my_message)
    send_entry.bind("<Return>", send_message)
    send_entry.place(x=0, y=400)

    send_button = Button(text=locale['send_button'], bg=default_bg, fg=default_fg, font=font_theme, command=send_message)
    send_button.place(x=520, y=420)

    if data['USER_SETTINGS']['THEME'] == 'light':
        default_fg = 'black'
        main.configure(bg='white')
        main.update()
        default_bg = 'white'
    elif data['USER_SETTINGS']['THEME'] == 'black':
        default_bg = 'black'
        main.configure(bg='black')
        main.update()
        default_fg = 'white'
    else:
        theme(data['USER_SETTINGS']['THEME'])


class Telemetry:
    def __init__(self, data_file):
        self.fl = data_file

    def write(self, a):
        if user_local_settings['USER_SETTINGS']['TELEMETRY_ENABLED'] == 'True':
            self.fl.write(a)
        else:
            self.fl.write('telemetry is off')

    def read(self):
        return self.fl.read()


def prog_credits():
    t_showinfo('Credits', 'Made with BTAE (BebraTech Application Engine) based on MSGR by BebraTech.\n'
                                                  'Author: Main Developer - zcveo.\n\n')


def create_custom_theme():
    theme_create = Tk()
    theme_create.configure(bg=default_bg)
    theme_create.resizable(False, False)
    theme_create.title(locale['cct_title'])
    Label(theme_create, text=locale['ct_bg'], bg=default_bg, fg=default_fg, font=font_theme).grid(column=0, row=0)
    Label(theme_create, text=locale['ct_fg'], bg=default_bg, fg=default_fg, font=font_theme).grid(column=0, row=1)
    Label(theme_create, text=locale['ct_fnt'], bg=default_bg, fg=default_fg, font=font_theme).grid(column=0, row=2)
    Label(theme_create, text=locale['name'], bg=default_bg, fg=default_fg, font=font_theme).grid(column=0, row=3)
    bg_ent = Entry(theme_create, width=30, bg=default_bg, fg=default_fg, font=font_theme)
    bg_ent.grid(column=1, row=0)
    fg_ent = Entry(theme_create, width=30, bg=default_bg, fg=default_fg, font=font_theme)
    fg_ent.grid(column=1, row=1)
    fnt_ent = Entry(theme_create, width=30, bg=default_bg, fg=default_fg, font=font_theme)
    fnt_ent.grid(column=1, row=2)
    fl_ent = Entry(theme_create, width=30, bg=default_bg, fg=default_fg, font=font_theme)
    fl_ent.grid(column=1, row=3)
    Button(theme_create, text=locale['cct_save'], command=lambda: save_theme(bg_ent.get(), fg_ent.get(), fnt_ent.get(), fl_ent.get()), bg=default_bg, fg=default_fg, font=font_theme).grid(column=0, row=4)


def save_theme(bg, fg, fnt, name):
    with open(f'./data/theme/{name}.theme', 'w') as th:
        if fnt == '':
            fnt = None
        if fg == '':
            fg = None
        if bg == '':
            bg = None
        if name == '':
            showerror(locale['error_title'], locale['cct_syntax_error'])
            return
        th.write(f'main_color={bg}\nsecondary_color={fg}\nfont={fnt}')
    reinit_window()


def select_server(a, w):
    global server, work
    server = a
    user_local_settings['USER_SETTINGS']['SERVER'] = a
    if w:
        w.destroy()
    work = False


def select_bt_server(a, w):
    global bt_server, work
    bt_server = a
    user_local_settings['USER_SETTINGS']['BT_SERV'] = a
    if w:
        w.destroy()
    work = False


def dump_data_nc():
    dat_d['[SETTINGS]'] = str(user_local_settings)
    with open('./data/DATA.NC', 'w', encoding='windows-1251') as fl:
        fl.write(encrypt(dat.dump(dat_d), eval(base_conf['CC'])))


def reload_data_nc():
    global dat, dat_d, user_local_settings, setting_raw, data
    global username, password, server, bt_server, lng
    try:
        dat = SNConfig(decrypt(open('./data/DATA.NC', 'r', encoding='windows-1251').read(), eval(base_conf['CC'])))
        dat_d = dat.load()
        setting_raw = dat_d['[SETTINGS]']
        user_local_settings = data = eval(setting_raw)
        username = user_local_settings['USER_SETTINGS']['USERNAME']
        password = user_local_settings['USER_SETTINGS']['PASSWORD']
        server = user_local_settings['USER_SETTINGS']['SERVER']
        bt_server = user_local_settings['USER_SETTINGS']['BT_SERV']
        lng = user_local_settings['USER_SETTINGS']['SEL_LOCALE']
    except Exception as nc_ex_rel:
        _show('Error', f'Error reloading DATA.NC. {type(nc_ex_rel)}')

def change_username(a):
    user_local_settings['USER_SETTINGS']['USERNAME'] = a


if 'run.pyw' in sys.argv[0]:
    print('MSGR QW BY BEBRA TECH, WITH BTAE')
    default_bg = 'black'
    default_fg = 'white'
    font_theme = ('Consolas', 9)
    debug_mode = False

    main = Tk()
    main.geometry('900x500')
    main.resizable(False, False)
    main.title('BTAE_BOOT')


    main.configure(bg='black')

    load_lbl = Label(main, text='Loading...', bg='black', fg='white',
                     font=('Consolas', 9), justify=LEFT)
    load_lbl.place(x=0, y=0)

    def printin_load_lbl(v, level='i'):
        if level == 'i':
            load_lbl['text'] += '\n' + v
        elif level == 'e':
            load_lbl['text'] += '\n' + v + '\n\nClick "Exit" to exit program.'
        main.update()

    Button(main, text='Exit', bg='black', fg='white',
                     font=('Consolas', 9), command=sys.exit).place(x=850, y=450)

    main.update()
    main.protocol('WM_DELETE_WINDOW', sys.exit)

    if 'BTAE!debugMode_ENABLE' in sys.argv:
        print('Debug Mode is enabled')
        debug_mode = True

    run_f_setup = False
    refresh = refresh1
    work = True
    last_obj_id = ''
    loading = True
    version = '0'
    encoding = 'UTF-8'
    files = ['./data/DATA.NC']
    base_conf = json.load(open('./data/base_data.json', 'r'))

    try:
        dat = SNConfig(decrypt(open('./data/DATA.NC', 'r', encoding='windows-1251').read(), eval(base_conf['CC'])))
        dat_d = dat.load()
    except Exception as _nc_ex:
        print(f'[py][fatal] data.nc not loaded, {_nc_ex}, {type(_nc_ex)}')
        showerror('Error1', 'DATA.NC damaged')
        sys.exit()
    try:
        setting_raw = dat_d['[SETTINGS]']
        user_local_settings = data = eval(setting_raw)
    except Exception as data_nc_load_ex:
        showerror('Error2', f'DATA.NC damaged, {data_nc_load_ex}')
        sys.exit()

    lng = user_local_settings['USER_SETTINGS']['SEL_LOCALE']
    print('[py][info] loading locale')
    try:
        locale_fl = Config(f'./data/locale/{lng}/locale.cfg', coding=encoding)
    except UnicodeDecodeError:
        encoding = 'windows-1251'
        locale_fl = Config(f'./data/locale/{lng}/locale.cfg', coding=encoding)
    locale = Locale(locale_fl)

    print(f'[py][info] locale_fl locale/{lng}/locale.cfg')
    print(f'[py][info] language {lng}')

    for i in sys.argv:
        if 'BootUpAction' in i:
            exec(i.split('$=%')[1])
        if 'BTAE!Debug_NotLoadObjects' in i:
            not_load_obj = i.split(':')[1].split()


    if data['USER_SETTINGS']['THEME'] == 'light':
        default_fg = 'black'
        main.configure(bg='white')
        main.update()
        default_bg = 'white'
    elif data['USER_SETTINGS']['THEME'] == 'black':
        default_bg = 'black'
        main.configure(bg='black')
        main.update()
        default_fg = 'white'
    else:
        try:
            theme(data['USER_SETTINGS']['THEME'])
        except NameError as theme_load_err:
            showerror('Error', f'main window is destroyed {theme_load_err}')
            sys.exit()

    main.configure(bg=default_bg)
    load_lbl.configure(bg=default_bg, fg=default_fg, font=font_theme)
    Button(main, text='Exit', bg=default_bg, fg=default_fg, font=font_theme, command=sys.exit).place(x=850, y=450)
    main.update()

    username = user_local_settings['USER_SETTINGS']['USERNAME']
    password = user_local_settings['USER_SETTINGS']['PASSWORD']
    server = user_local_settings['USER_SETTINGS']['SERVER']
    bt_server = user_local_settings['USER_SETTINGS']['BT_SERV']
    hash_method = user_local_settings['USER_SETTINGS']['HASHING_METHOD']


    if eval(dat_d['[SETTINGS]'])['USER_SETTINGS']['FIRST_BOOT'] == 'True':
        policy_win = Tk()
        policy_win.title('User Policy Agreement')
        Label(policy_win, text='Please agree with user policy', font=('Consolas', 10)).pack()
        Button(policy_win, text='BebraTech Agreement (Credits)', command=prog_credits, font=('Consolas', 10)).pack()
        Button(policy_win, text='BTAEML Agreement', command=lambda: exec('import plugins.core.mod\nplugins.core.mod.plugin_info()'), font=('Consolas', 10)).pack()
        Button(policy_win, text='Continue', command=lambda: exec('policy_win.quit()\npolicy_win.destroy()'), font=('Consolas', 10)).pack()
        policy_win.mainloop()


    print(bt_server, server)
    if bt_server == '' or server == '':
        printin_load_lbl('Please, select server')

        def select_servers(a, b, win):
            if b:
                select_bt_server(b, None)
            if a:
                select_server(a, win)
            dump_data_nc()
            reload_data_nc()
            server_select_win.quit()
            server_select_win.destroy()
        server_select_win = Tk()
        server_select_win.title(locale['server_select_win'])
        server_select_win.resizable(False, False)
        Label(server_select_win, text=locale['servers_setup_title']).pack()
        server_entry = Entry(server_select_win, width=50)
        if server == '':
            server_entry.pack()
        else:
            Label(server_select_win, text=locale['serv_selected_alr']).pack()
        bt_server_entry = Entry(server_select_win, width=50)
        if bt_server == '':
            bt_server_entry.pack()
        else:
            Label(server_select_win, text=locale['bt_serv_selected_alr']).pack()
        Button(server_select_win, text=locale['conf_server'], command=lambda: select_servers(server_entry.get(), bt_server_entry.get(), server_select_win)).pack()
        server_select_win.mainloop()

    print('cont')

    if username == '' or password == '':
        printin_load_lbl('Please, login/register in your account')
        def conf_login(a, b, win):
            user_local_settings['USER_SETTINGS']['USERNAME'] = a
            if b != '':
                hs = hashlib.new(hash_method)
                hs.update(b.encode())
                user_local_settings['USER_SETTINGS']['PASSWORD'] = hs.hexdigest()
            else:
                user_local_settings['USER_SETTINGS']['PASSWORD'] = ' '
            win.destroy()
            dump_data_nc()
            reload_data_nc()
            printin_load_lbl('Restart is required')

        login_win = Tk()
        login_win.title(locale['login_txt'])
        login_win.resizable(False, False)
        Label(login_win, text=locale['login_hint']).pack()
        usr_entry = Entry(login_win, width=30)
        usr_entry.pack()
        passw_entry = Entry(login_win, width=30)
        passw_entry.pack()
        Button(login_win, text=locale['conf_login_tex'], command=lambda: conf_login(usr_entry.get(), passw_entry.get(), login_win)).pack()
        login_win.mainloop()

    if not run_f_setup:
        printin_load_lbl('Connecting to account...')
        try:
            print('connecting to account...')
            user = auth.User(username, password, bt_server.split(':')[0], int(bt_server.split(':')[1]))
            try:
                bt_server_data = user.get_data()
            except AttributeError:
                bt_server_data = (False, {})
            print('bt data')
            print(bt_server_data)
            if not bt_server_data[0] and bt_server_data[1] != 'password':
                printin_load_lbl('Not connected to BebraTech Authentication Server', 'e')
                if debug_mode:
                    load_lbl['text'] += f'\nDebug Info:\nbt_server_data[0] is False, means Unknown Error.\n{bt_server_data}'
                select_bt_server('', None)
                dump_data_nc()
                main.mainloop()
            elif bt_server_data[1] == 'password':
                user_local_settings['USER_SETTINGS']['PASSWORD'] = ''
                user_local_settings['USER_SETTINGS']['USERNAME'] = ''
                dump_data_nc()
                printin_load_lbl('Incorrect Password', 'e')
                if debug_mode:
                    load_lbl['text'] += f'\nDebug Info:\njust incorrect password for acc {username}, {bt_server_data}, {password}'
                main.mainloop()

        except (ConnectionError, IndexError):
            printin_load_lbl(f'Not connected to BebraTech Authentication Server: Server on {bt_server} not found.', 'e')
            if debug_mode:
                load_lbl[
                    'text'] += f'\nDebug Info:\nIncorrect IP in <bt_server> variable.'
            select_bt_server('', None)
            dump_data_nc()
            main.mainloop()


        try:
            printin_load_lbl('Connecting to Chat...')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server.split(':')[0], int(server.split(':')[1])))
            receive_thread = threading.Thread(target=receive_messages)
        except Exception as chat_err:
            print(type(chat_err))
            printin_load_lbl(f'Not connected to Chatting Server: Server on {server} not found.', 'e')
            if debug_mode:
                load_lbl[
                    'text'] += f'\nDebug Info:\nIncorrect IP in <server> variable.'
            select_server('', None)
            dump_data_nc()
            main.mainloop()

    history = []

    my_message = StringVar()
    send_entry = Entry()

    if user_local_settings['USER_SETTINGS']['BTAEML'] == 'True':
        from plugins.core.mod import autoload_objects, get_plugs
        print('LOAD BTAEML')

    try:
        _plugin_objects = get_plugs()
    except (NameError, FileNotFoundError):
        _plugin_objects = {}

    exc_chf = SConfig(dat_d['[LOADER_CONFIG]'])

    os.chdir(os.path.dirname(os.path.realpath(__file__)))


    if eval(dat_d['[SETTINGS]'])['USER_SETTINGS']['FIRST_BOOT'] == 'True':
        user_local_settings['USER_SETTINGS']['FIRST_BOOT'] = 'False'
        run_f_setup = True


    try:
        print('[py][info] loading plugins')
        autoload_objects(_plugin_objects)
        print('[py][info] completed')
    except NameError:
        print('[py][warning] not detected plugin_api module')
        pass


    # init theme

    if data['USER_SETTINGS']['THEME'] == 'light':
        default_fg = 'black'
        main.configure(bg='white')
        main.update()
        default_bg = 'white'
    elif data['USER_SETTINGS']['THEME'] == 'black':
        default_bg = 'black'
        main.configure(bg='black')
        main.update()
        default_fg = 'white'
    else:
        theme(data['USER_SETTINGS']['THEME'])

    loading = False

    main.protocol("WM_DELETE_WINDOW", shutdown)

    if run_f_setup:
        FirstSetup(default_bg, default_fg, font_theme, locale, theme, refresh_locale_easy).get_win()
        dump_data_nc()
        reload_data_nc()


    load_lbl.destroy()
    reinit_window()


    for i in sys.argv:
        if 'StartUpAction' in i:
            exec(i.split('$=%')[1])
    if bt_server_data[1] != 'blocked':
        chat_window = Text(fg=default_fg, bg=default_bg, font=font_theme, width=110)
        chat_window.place(x=0, y=0)
    if not run_f_setup and work and bt_server_data[1] != 'blocked':
        receive_thread.start()
        if '_show_ip' not in bt_server_data[1]['answer']:
            auth.update_personal_conf(username, ['_show_ip', 'False'])
            relog()
    main.configure(bg=default_bg)
    main.title(locale['WINDOW_TITLE_TEXT'])
    if work:
        try:
            main.mainloop()
        except KeyboardInterrupt:
            main.destroy()

    os.system('rmdir __pycache__ /s /q')

    dat_d['[SETTINGS]'] = str(user_local_settings)
    with open('./data/DATA.NC', 'w', encoding='windows-1251') as fl:
        fl.write(encrypt(dat.dump(dat_d), eval(base_conf['CC'])))

print('finish')