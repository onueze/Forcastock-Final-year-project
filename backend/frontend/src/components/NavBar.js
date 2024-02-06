import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import {Link, useLocation} from 'react-router-dom';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import LoginIcon from '@mui/icons-material/Login';
import BorderColorIcon from '@mui/icons-material/BorderColor';

const drawerWidth = 240;

export default function Navbar() {
    const location = useLocation();
    const path = location.pathname
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Forcastock
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            
              <ListItem key={text} disablePadding>
                <ListItemButton component={Link} to="/" selected= {"/" === path}>
                  <ListItemIcon>
                        <HomeIcon/>
                  </ListItemIcon>
                  <ListItemText primary={"Landing"} />
                </ListItemButton>
              </ListItem>

              <ListItem key={text} disablePadding>
                <ListItemButton component={Link} to="/home" selected= {"/home" === path}>
                  <ListItemIcon>
                        <HomeIcon/>
                  </ListItemIcon>
                  <ListItemText primary={"Home"} />
                </ListItemButton>
              </ListItem>

              <ListItem key={text} disablePadding>
                <ListItemButton component={Link} to="/login" selected= {"/login" === path}>
                  <ListItemIcon>
                        <LoginIcon/>
                  </ListItemIcon>
                  <ListItemText primary={"Login"} />
                </ListItemButton>
              </ListItem>


              <ListItem key={text} disablePadding>
                <ListItemButton component={Link} to="/register" selected= {"/register" === path}>
                  <ListItemIcon>
                        <BorderColorIcon/>
                  </ListItemIcon>
                  <ListItemText primary={"Register"} />
                </ListItemButton>
              </ListItem>


          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
      </Box>
    </Box>
  );
}