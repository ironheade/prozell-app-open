import React, { useState } from 'react';
import {
  Header,
  HeaderContainer,
  HeaderName,
  HeaderNavigation,
  HeaderMenuButton,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent,
  SideNav,
  SideNavItems,
  HeaderSideNavItems
} from 'carbon-components-react';
import { UserAvatar24 } from '@carbon/icons-react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import LoginModal from './loginModal';


const TutorialHeader = () => {
  const logged = useSelector(state => state.loggedIn)
  const [ loginModalOpen, setLoginModalOpen ] = useState(false)

  return (
    <HeaderContainer
      render={({ isSideNavExpanded, onClickSideNavExpand }) => (
        <Header aria-label="Carbon Tutorial">
          <SkipToContent />
          <HeaderMenuButton
            aria-label="Open menu"
            isCollapsible
            onClick={onClickSideNavExpand}
            isActive={isSideNavExpanded}
          />
          <HeaderName element={Link} to="/" prefix="IPAT">
            ProZell Kostenrechner
          </HeaderName>
          {logged &&
            <HeaderNavigation aria-label="Carbon Tutorial">
              <HeaderMenuItem element={Link} to="/Zellauslegung">
                Zellauslegung
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/Prozessauslegung">
                Prozessauslegung
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/AllgemeineParameter">
                Allgemeine Parameter
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/Ergebnisse">
                Ergebnisse
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/AdminPage">
                Admin Seite
              </HeaderMenuItem>
            </HeaderNavigation>
          }
          {logged &&
            <SideNav
              aria-label="Side navigation"
              expanded={isSideNavExpanded}

              isPersistent={false}
            >
              <SideNavItems>

                <HeaderSideNavItems>
                  <HeaderMenuItem element={Link} to="/">
                    Startseite
                  </HeaderMenuItem>
                  <HeaderMenuItem element={Link} to="/Zellauslegung">
                    Zellauslegung
                  </HeaderMenuItem>
                  <HeaderMenuItem element={Link} to="/Prozessauslegung">
                    Prozessauslegung
                  </HeaderMenuItem>
                  <HeaderMenuItem element={Link} to="/AllgemeineParameter">
                    Allgemeine Parameter
                  </HeaderMenuItem>
                  <HeaderMenuItem element={Link} to="/Ergebnisse">
                    Ergebnisse
                  </HeaderMenuItem>
                  <HeaderMenuItem element={Link} to="/AdminPage">
                    Admin Seite
                  </HeaderMenuItem>
                </HeaderSideNavItems>

              </SideNavItems>
            </SideNav>
          }
          <HeaderGlobalBar>

            <HeaderGlobalAction aria-label="User Avatar" onClick={() => setLoginModalOpen(true)}>
              <UserAvatar24 />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
          <LoginModal open={loginModalOpen} close={()=>setLoginModalOpen(false)}/>

        </Header>

      )}
    />
  )
}



export default TutorialHeader;
